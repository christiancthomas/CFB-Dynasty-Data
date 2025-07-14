"""
Geographic visualizations and heatmaps for CFB Dynasty analysis.

This module provides functions to create interactive geographic visualizations
including state heatmaps and city-level analysis.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from .geocoding import get_city_coordinates


def create_geographic_heatmap(df):
    """
    Create a geographic heatmap showing player distribution across the US.

    Args:
        df (pandas.DataFrame): Roster dataframe with 'CITY' and 'STATE' columns

    Returns:
        plotly.graph_objects.Figure: The geographic heatmap figure, or None if failed
    """
    # Check if geographic columns exist
    if 'CITY' not in df.columns or 'STATE' not in df.columns:
        print("⚠️  Geographic heatmap requires 'CITY' and 'STATE' columns in your data")
        print("📝 Sample data structure needed:")
        print("   FIRST NAME | LAST NAME | POSITION | CITY        | STATE")
        print("   John       | Smith     | QB       | Atlanta     | GA")
        print("   Mike       | Johnson   | RB       | Dallas      | TX")
        return None

    try:
        # Count players by state
        state_counts = df['STATE'].value_counts().reset_index()
        state_counts.columns = ['state', 'player_count']

        # Create choropleth map
        fig = go.Figure(data=go.Choropleth(
            locations=state_counts['state'],
            z=state_counts['player_count'],
            locationmode='USA-states',
            colorscale='Reds',
            text=state_counts['state'],
            marker_line_color='white',
            colorbar_title="Players"
        ))

        fig.update_layout(
            title='🗺️ Player Geographic Distribution - US Heatmap',
            geo=dict(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'
            ),
            height=600
        )

        # Add city pins using automatic geocoding with enhanced timeout handling
        if df['CITY'].notna().sum() > 0:
            city_state_counts = df.groupby(['CITY', 'STATE']).size().reset_index(name='player_count')

            # Get coordinates for all cities automatically
            city_lats, city_lons, city_names, city_counts, city_texts = [], [], [], [], []
            print(f"🗺️ Geocoding {len(city_state_counts)} cities...")

            for _, row in city_state_counts.iterrows():
                city_name = row['CITY']
                state_name = row['STATE']
                coords = get_city_coordinates(city_name, state_name)

                if coords:
                    lat, lon = coords
                    city_lats.append(lat)
                    city_lons.append(lon)
                    city_names.append(f"{city_name}, {state_name}")
                    city_counts.append(row['player_count'])
                    city_texts.append(f"{city_name}, {state_name}<br>{row['player_count']} player(s)")

            # Add city pins to the map
            if city_lats:
                fig.add_trace(go.Scattergeo(
                    locationmode='USA-states',
                    lon=city_lons,
                    lat=city_lats,
                    text=city_texts,
                    mode='markers',
                    marker=dict(
                        size=[count * 3 + 8 for count in city_counts],  # Scale marker size by player count
                        color='darkblue',
                        opacity=0.8,
                        line=dict(width=2, color='white'),
                        symbol='circle'
                    ),
                    name='Cities',
                    hovertemplate='%{text}<extra></extra>'
                ))
                print(f"📍 Successfully plotted {len(city_lats)} cities on map")

        fig.show()

        # Create city-level bar chart
        create_city_bar_chart(df)

        # Print summary statistics
        print("🗺️ Geographic Distribution Summary:")
        print(f"  • Total States Represented: {df['STATE'].nunique()}")
        print(f"  • Total Cities Represented: {df['CITY'].nunique()}")
        print(f"  • Top 5 States by Player Count:")

        top_states = df['STATE'].value_counts().head(5)
        for state, count in top_states.items():
            print(f"    - {state}: {count} players")

        return fig

    except Exception as e:
        print(f"❌ Error creating geographic heatmap: {e}")
        return None


def create_city_bar_chart(df):
    """
    Create a horizontal bar chart showing top cities by player count.

    Args:
        df (pandas.DataFrame): Roster dataframe with 'CITY' and 'STATE' columns

    Returns:
        plotly.graph_objects.Figure: The bar chart figure, or None if failed
    """
    try:
        if df['CITY'].notna().sum() > 0:
            city_state_counts = df.groupby(['CITY', 'STATE']).size().reset_index(name='player_count')
            city_state_counts = city_state_counts.sort_values('player_count', ascending=False).head(20)

            fig2 = px.bar(
                city_state_counts.head(15),
                x='player_count',
                y=[f"{row['CITY']}, {row['STATE']}" for _, row in city_state_counts.head(15).iterrows()],
                orientation='h',
                title='🏙️ Top 15 Cities by Player Count',
                labels={'player_count': 'Number of Players', 'y': 'City, State'}
            )

            fig2.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
            fig2.show()

            return fig2

    except Exception as e:
        print(f"❌ Error creating city bar chart: {e}")
        return None
