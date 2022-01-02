import dash
from dash import dcc
from dash import html
import dash as dtable
from dash.dependencies import Input, Output
import plotly.express as px
import json
import networkx as nx
import plotly.graph_objects as go
import scaffoldgraph as sg

#df['seg_id'] = [str(x) for x in df['seg_id']]
#seg_ids = df['seg_id'].unique()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

#fig = px.scatter_3d(df, x="x", y="y",z="z", color="user", custom_data=["seg_id"])

#fig.update_layout(clickmode='event+select')
####
A = nx.read_gml('chemApp/raw_files/Benzene.gml')
for node in A.nodes():
    position_string = A.nodes[node]['position']
    A.nodes[node]['pos'] = [float(x) for x in position_string.split()]
    if not A.nodes[node]['text']:
        A.nodes[node]['text'] = 'C'


edge_x = []
edge_y = []
for edge in A.edges():
    x0, y0 = A.nodes[edge[0]]['pos']
    x1, y1 = A.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in A.nodes():
    x, y = A.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        
        line_width=2))


node_adjacencies = []
node_text = []
for node, adjacencies in enumerate(A.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: '+str(len(adjacencies[1])))

node_trace.marker.color = node_adjacencies
node_trace.text = node_text

fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='<br>Network graph made with Python',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
from PIL import Image
pyLogo = Image.open('chemApp/visualizations/benzene.png')
fig.add_layout_image(
        source=pyLogo,
        xref="x domain",
        yref="y domain",
        x=0,
        y=0,
        xanchor="left",
        yanchor="bottom",
        sizing= "stretch",
        sizex=1,
        sizey=1,
        layer= "below"
    )
fig.update_layout(
    autosize=False,
    width=490,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
)

####


app.layout = html.Div([
    html.Div([
        dcc.Graph(
            id='basic-interactions',
            figure=fig,
            style={'width': '100%', 'height': '90vh'}
        ),
    ], style={
        'padding': '10px 5px',
        'float':'left',
        'width':'60vw',
    }),

    html.Div( 
    style={'width':'35vw', 
            'flex-direction':'column',
            'float':'right',
            'overflow':'scroll'},
    children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**

                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ],style={'padding':'1vh 1vw'}),

        html.Div([
            dcc.Markdown("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.

                Note that if `layout.clickmode = 'event+select'`, selection data also
                accumulates (or un-accumulates) selected data if you hold down the shift
                button while clicking.
            """),
            html.Pre(id='selected-data', style=styles['pre']),
        ],style={'padding':'1vh 1vw'}),

    ])
])

@app.callback(
    Output('hover-data', 'children'),
    Input('basic-interactions', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)
"""
@app.callback(
    dash.dependencies.Output('basic-interactions', 'figure'),
    [dash.dependencies.Input('crossfilter_seg_id', 'value')])
def update_graph(crossfilter_seg_id):
    dff = df[df['seg_id'] == crossfilter_seg_id]
    fig = px.scatter_3d(dff, x="x", y="y",z="z", color="user", custom_data=["seg_id"])
    return fig

@app.callback(
    Output('click-data', 'children'),
    Input('basic-interactions', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)
"""
@app.callback(
    Output('selected-data', 'children'),
    Input('basic-interactions', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)

if __name__ == '__main__':
    app.run_server(debug=True)