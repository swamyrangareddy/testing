import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

# Set the title of the app
st.title("Data Visualization App")

# Step 1: Upload a file
uploaded_file = st.file_uploader("Upload your Excel or CSV file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Step 2: Read the file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Display the dataframe
    st.write("Uploaded Data:")
    with st.expander("View Data"):
        st.dataframe(df)

    # Step 3: Sidebar for graph type and column selection
    st.sidebar.header("Graph Options")

    # Graph type selection
    graph_type = st.sidebar.selectbox(
        "Select the type of graph",
        ["Bar Chart", "Line Chart","Pie Chart", "Scatter Plot", "Area Chart","altair_chart","vega_lite_chart","plotly_chart"]
    )

    # Column selection based on graph type
    columns = df.columns.tolist()

    if graph_type in ["Bar Chart", "Line Chart", "Area Chart"]:
        x_axis = st.sidebar.selectbox("Select X-axis", columns, index=0)
        y_axis = st.sidebar.selectbox("Select Y-axis", columns, index=1)
    elif graph_type == "Scatter Plot" or graph_type in ["altair_chart", "vega_lite_chart", "plotly_chart", "Pie Chart"]:
        x_axis = st.sidebar.selectbox("Select X-axis", columns, index=0)
        y_axis = st.sidebar.selectbox("Select Y-axis", columns, index=1)

    # Step 4: Select number of rows to display
    num_rows = st.sidebar.slider("Select number of rows to display", min_value=1, max_value=len(df), value=len(df))

    # Filter the dataframe based on the selected number of rows
    df = df.head(num_rows)

    # Step 5: Generate the selected graph
    st.write(f"### {graph_type}")

    if graph_type == "Bar Chart":
        st.bar_chart(df[[x_axis, y_axis]].set_index(x_axis))

    elif graph_type == "Line Chart":
        st.line_chart(df[[x_axis, y_axis]].set_index(x_axis))

    elif graph_type == "Scatter Plot":
        st.scatter_chart(df[[x_axis, y_axis]])

    elif graph_type == "Area Chart":
        st.area_chart(df[[x_axis, y_axis]].set_index(x_axis))
    
    # # altair_chart 
    #     chart = alt.Chart(df).mark_line().encode(
    #         x=x_axis,
    #         y=y_axis
    #     )
    #     st.altair_chart(chart)
    #     st.altair_chart(df[[x_axis, y_axis]].set_index(x_axis))
    
    # vega_lite_chart
    elif graph_type == "vega_lite_chart":
        spec = {
            'mark': 'line',
            'encoding': {
                'x': {'field': x_axis, 'type': 'quantitative'},
                'y': {'field': y_axis, 'type': 'quantitative'}
            }
        }
        st.vega_lite_chart(df, spec=spec, use_container_width=True)

    # plotly_chart
    elif graph_type == "plotly_chart":
        fig = px.line(df, x=x_axis, y=y_axis)  # You can change 'px.line' to other plotly express functions based on your needs
        st.plotly_chart(fig)
    
    # Pie Chart
    elif graph_type == "Pie Chart":
        fig = px.pie(df, names=x_axis, values=y_axis)
        st.plotly_chart(fig)