"""
Recruiting territory analysis for CFB Dynasty.

This module provides functions to analyze recruiting success by geographic region
and create visualizations showing recruiting territory performance.
"""

import plotly.graph_objects as go


def create_recruiting_territory_map(df):
    """
    Create a map showing recruiting territories and success by region.

    Args:
        df (pandas.DataFrame): Roster dataframe with geographic and player data

    Returns:
        plotly.graph_objects.Figure: The recruiting territory map, or None if failed
    """
    if 'CITY' not in df.columns or 'STATE' not in df.columns:
        print("⚠️  Recruiting territory map requires 'CITY' and 'STATE' columns")
        return None

    try:
        # Calculate recruiting metrics by state
        state_metrics = df.groupby('STATE').agg({
            'VALUE': ['count', 'mean', 'max'],
            'DEV TRAIT': lambda x: (x == 'ELITE').sum() + (x == 'STAR').sum()
        }).round(2)

        state_metrics.columns = ['player_count', 'avg_value', 'max_value', 'elite_star_count']
        state_metrics = state_metrics.reset_index()

        # Create recruiting success heatmap
        fig = go.Figure(data=go.Choropleth(
            locations=state_metrics['STATE'],
            z=state_metrics['avg_value'],
            locationmode='USA-states',
            colorscale='RdYlGn',
            text=[f"{state}<br>Avg Value: {avg_val}<br>Players: {count}<br>Elite/Star: {elite}"
                  for state, avg_val, count, elite in zip(
                      state_metrics['STATE'],
                      state_metrics['avg_value'],
                      state_metrics['player_count'],
                      state_metrics['elite_star_count']
                  )],
            hovertemplate='%{text}<extra></extra>',
            marker_line_color='white',
            colorbar_title="Avg Player Value"
        ))

        fig.update_layout(
            title='🎯 Recruiting Territory Success Map - Average Player Value by State',
            geo=dict(
                scope='usa',
                projection=go.layout.geo.Projection(type='albers usa'),
                showlakes=True,
                lakecolor='rgb(255, 255, 255)'
            ),
            height=600
        )

        fig.show()

        print("🎯 Recruiting Territory Analysis:")
        print(f"  • Best Recruiting State (Avg Value): {state_metrics.loc[state_metrics['avg_value'].idxmax(), 'STATE']}")
        print(f"  • Most Players from: {state_metrics.loc[state_metrics['player_count'].idxmax(), 'STATE']}")
        print(f"  • Most Elite/Star Players from: {state_metrics.loc[state_metrics['elite_star_count'].idxmax(), 'STATE']}")

        return fig

    except Exception as e:
        print(f"❌ Error creating recruiting territory map: {e}")
        return None
