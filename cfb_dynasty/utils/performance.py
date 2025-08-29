"""Performance optimizations for CFB Dynasty Data system."""

import pandas as pd
import functools
import time
from typing import Dict, Any, List
from ..utils.log import get_logger

logger = get_logger(__name__)


def timer_decorator(func):
    """Decorator to time function execution."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.debug(f"{func.__name__} executed in {end_time - start_time:.2f} seconds")
        return result
    return wrapper


class DataFrameOptimizer:
    """Optimize DataFrame operations for better performance."""
    
    @staticmethod
    def optimize_datatypes(df: pd.DataFrame) -> pd.DataFrame:
        """Optimize DataFrame column data types for memory efficiency."""
        optimized_df = df.copy()
        
        for col in optimized_df.columns:
            # Convert boolean-like columns
            if optimized_df[col].dtype == 'object':
                unique_values = set(optimized_df[col].dropna().unique())
                if unique_values.issubset({True, False, 'True', 'False', 'true', 'false', 1, 0}):
                    optimized_df[col] = optimized_df[col].astype('bool')
                    logger.debug(f"Converted {col} to boolean")
                
            # Convert numeric columns to more efficient types
            elif optimized_df[col].dtype in ['int64', 'float64']:
                if optimized_df[col].dtype == 'int64':
                    if optimized_df[col].min() >= 0 and optimized_df[col].max() <= 255:
                        optimized_df[col] = optimized_df[col].astype('uint8')
                    elif optimized_df[col].min() >= -32768 and optimized_df[col].max() <= 32767:
                        optimized_df[col] = optimized_df[col].astype('int16')
                    elif optimized_df[col].min() >= -2147483648 and optimized_df[col].max() <= 2147483647:
                        optimized_df[col] = optimized_df[col].astype('int32')
                
                elif optimized_df[col].dtype == 'float64':
                    if optimized_df[col].notna().all():  # No NaN values
                        optimized_df[col] = pd.to_numeric(optimized_df[col], downcast='float')
        
        return optimized_df
    
    @staticmethod
    def create_categorical_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        """Convert specified columns to categorical for memory efficiency."""
        optimized_df = df.copy()
        
        for col in columns:
            if col in optimized_df.columns:
                optimized_df[col] = optimized_df[col].astype('category')
                logger.debug(f"Converted {col} to categorical")
        
        return optimized_df


class AnalysisCache:
    """Simple caching system for expensive operations."""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._timestamps: Dict[str, float] = {}
        self.max_age = 3600  # 1 hour cache expiration
    
    def get(self, key: str) -> Any:
        """Get cached value if it exists and is not expired."""
        if key in self._cache:
            if time.time() - self._timestamps[key] < self.max_age:
                logger.debug(f"Cache hit for {key}")
                return self._cache[key]
            else:
                # Expired, remove from cache
                del self._cache[key]
                del self._timestamps[key]
                logger.debug(f"Cache expired for {key}")
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Set cached value with timestamp."""
        self._cache[key] = value
        self._timestamps[key] = time.time()
        logger.debug(f"Cached {key}")
    
    def clear(self) -> None:
        """Clear all cached values."""
        self._cache.clear()
        self._timestamps.clear()
        logger.debug("Cache cleared")


# Global cache instance
analysis_cache = AnalysisCache()


@timer_decorator
def optimized_value_calculation(df: pd.DataFrame) -> pd.DataFrame:
    """Optimized version of player value calculation for large datasets."""
    from ..config.constants import DEV_TRAIT_MULTIPLIERS, REMAINING_YEARS, RS_DISCOUNT
    
    # Cache key based on DataFrame hash
    cache_key = f"value_calc_{hash(pd.util.hash_pandas_object(df).sum())}"
    cached_result = analysis_cache.get(cache_key)
    
    if cached_result is not None:
        return cached_result
    
    # Optimize DataFrame
    optimized_df = DataFrameOptimizer.optimize_datatypes(df.copy())
    
    # Vectorized operations
    dev_multipliers = optimized_df['DEV TRAIT'].map(DEV_TRAIT_MULTIPLIERS).fillna(1.0)
    remaining_years = optimized_df['YEAR'].map(REMAINING_YEARS).fillna(0)
    
    # Handle both column name formats
    base_rating = optimized_df.get('BASE RATING', optimized_df.get('BASE OVERALL', 0))
    
    # Vectorized redshirt discount calculation
    redshirt_discount = optimized_df['YEAR'].str.contains(r'\(RS\)', na=False) * RS_DISCOUNT
    
    # Calculate values in one vectorized operation
    values = (
        base_rating * dev_multipliers * 
        (1 + remaining_years / 4) * 
        (1 - redshirt_discount)
    ).round(2)
    
    optimized_df['VALUE'] = values
    
    # Cache the result
    analysis_cache.set(cache_key, optimized_df)
    
    return optimized_df


def batch_process_rosters(roster_files: List[str], batch_size: int = 10) -> List[pd.DataFrame]:
    """Process multiple roster files in batches to manage memory."""
    results = []
    
    for i in range(0, len(roster_files), batch_size):
        batch = roster_files[i:i + batch_size]
        logger.info(f"Processing batch {i//batch_size + 1} ({len(batch)} files)")
        
        batch_results = []
        for file_path in batch:
            try:
                df = pd.read_csv(file_path)
                df = optimized_value_calculation(df)
                batch_results.append(df)
            except Exception as e:
                logger.error(f"Error processing {file_path}: {e}")
                continue
        
        results.extend(batch_results)
        
        # Clear memory after each batch
        if i % (batch_size * 3) == 0:  # Every 3 batches
            analysis_cache.clear()
    
    return results


class PerformanceProfiler:
    """Simple profiler for identifying performance bottlenecks."""
    
    def __init__(self):
        self.timings: Dict[str, List[float]] = {}
    
    def time_function(self, func_name: str, func, *args, **kwargs):
        """Time a function call and store the result."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        if func_name not in self.timings:
            self.timings[func_name] = []
        self.timings[func_name].append(execution_time)
        
        return result
    
    def get_stats(self) -> Dict[str, Dict[str, float]]:
        """Get performance statistics."""
        stats = {}
        for func_name, times in self.timings.items():
            stats[func_name] = {
                'total': sum(times),
                'average': sum(times) / len(times),
                'min': min(times),
                'max': max(times),
                'calls': len(times)
            }
        return stats
    
    def print_report(self):
        """Print performance report."""
        print("\n📊 PERFORMANCE REPORT")
        print("=" * 40)
        
        stats = self.get_stats()
        sorted_funcs = sorted(stats.items(), key=lambda x: x[1]['total'], reverse=True)
        
        for func_name, func_stats in sorted_funcs:
            print(f"\n🔧 {func_name}:")
            print(f"   Total time: {func_stats['total']:.2f}s")
            print(f"   Average: {func_stats['average']:.3f}s")
            print(f"   Calls: {func_stats['calls']}")
            print(f"   Range: {func_stats['min']:.3f}s - {func_stats['max']:.3f}s")


# Global profiler instance
performance_profiler = PerformanceProfiler()


def optimize_for_large_datasets(df: pd.DataFrame, threshold: int = 1000) -> pd.DataFrame:
    """Apply optimizations for large datasets."""
    if len(df) < threshold:
        return df  # Small dataset, no optimization needed
    
    logger.info(f"Optimizing large dataset with {len(df)} rows")
    
    # Apply optimizations
    optimized_df = DataFrameOptimizer.optimize_datatypes(df)
    
    # Convert position and other categorical columns
    categorical_columns = ['POSITION', 'YEAR', 'DEV TRAIT', 'ARCHETYPE', 'STATUS']
    optimized_df = DataFrameOptimizer.create_categorical_columns(optimized_df, categorical_columns)
    
    return optimized_df


def memory_usage_report(df: pd.DataFrame) -> None:
    """Print memory usage report for a DataFrame."""
    memory_usage = df.memory_usage(deep=True)
    total_memory = memory_usage.sum()
    
    print(f"\n💾 MEMORY USAGE REPORT")
    print("=" * 30)
    print(f"Total memory: {total_memory / 1024 / 1024:.2f} MB")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Memory per row: {total_memory / len(df):.1f} bytes")
    
    # Show top memory consuming columns
    print("\nTop memory consuming columns:")
    sorted_usage = memory_usage.sort_values(ascending=False).head(5)
    for col, usage in sorted_usage.items():
        if col != 'Index':
            print(f"   {col}: {usage / 1024:.1f} KB ({df[col].dtype})")


# Convenience function to enable all optimizations
def enable_performance_mode(df: pd.DataFrame) -> pd.DataFrame:
    """Enable all performance optimizations for a DataFrame."""
    logger.info("Enabling performance mode")
    
    # Apply all optimizations
    optimized_df = optimize_for_large_datasets(df)
    
    # Print memory report
    if logger.isEnabledFor(20):  # INFO level
        memory_usage_report(optimized_df)
    
    return optimized_df
