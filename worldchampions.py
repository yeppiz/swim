import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

swim = pd.read_csv("Olympic_Swimming_Results_1912to2020.csv")
# drop empty values
swim = swim.dropna()
# process results in seconds

processed = []
for result in swim["Results"]:
    if "est" in result:
        result = result.replace("est", "")
    if(result[0].isnumeric()):
        splitt = result.split(":")
        if len(splitt) == 1:
            processed.append(float(splitt[0]))
        elif len(splitt) == 2:
            processed.append(int(splitt[0]) * 60 + float(splitt[1]))
        else:
            processed.append(int(splitt[1]) * 60 + float(splitt[2]))
    else:
        processed.append("-1")
swim["ProcessedTime"] = processed

mask = swim["Rank"] == 1
swim1 = swim[mask]
swimbar = swim1.groupby("Team")["Results"].count().reset_index()
swimbar = swimbar.sort_values("Results", ascending=False)

athlete = swim1.groupby("Athlete").count().reset_index()
mask = athlete["Location"] >= 3
count = athlete[mask]



st.title("data exploration project")

st.title("Data Analysis")
st.markdown("The data is shown below: ")
st.sidebar.title("Options")
st.sidebar.markdown("Select Charts and Features:")
# st.dataframe(df)
option = st.sidebar.selectbox("World Champions by Country", ["None", "bar chart", "map", "pie", "sunburst", "line"])
if option == "bar chart":
    category1 = st.sidebar.selectbox("Which category would you like to see?", ["None", "team results", "athlete results"])
    st.markdown(category1)
    if category1 == "team results":
        fig = px.bar(swimbar, x = "Team", y = "Results")
        st.plotly_chart(fig)
    else:
        abar = swim1.groupby("Athlete")["Results"].count().reset_index()
        abar = abar.sort_values("Results", ascending=False)
        fig = px.bar(abar, x="Athlete", y="Results")
        st.plotly_chart(fig)
elif option == "map":
    fig = px.scatter_geo(swimbar, locations='Team',
                         hover_name='Team',
                         size='Results',
                         size_max=70,
                         projection='natural earth',
                         width=1000,
                         height=600)
    st.plotly_chart(fig)
elif option == "pie":
    fig = px.pie(count, values = "Results", names = "Athlete")
    st.plotly_chart(fig)
elif option == "sunburst":
    st.markdown("This chart divides all data by gender, event, and distance.")
    groups = swim1.groupby(["Gender", "Stroke", "Team", "Distance (in meters)", "Athlete"]).size().reset_index(
        name="count")
    fig = px.sunburst(groups, path = ["Gender", "Stroke", "Distance (in meters)", "Athlete"], height=600)
    st.plotly_chart(fig)
elif option == "line":
    category = st.sidebar.selectbox("Which distance would you like to see?", ["None", "50m", "100m", "200m", "400m", "800m", "1500m", "4x100", "4x200"])
    category2 = st.sidebar.selectbox("Which stroke would you like to see?", ["None", "Freestyle", "Backstroke", "Butterfly", "Breaststroke", "Individual medley", "Medley"])
    st.markdown(category)
    st.markdown(category2)
    mask1 = swim1["Distance (in meters)"] == category
    mask2 = swim1["Stroke"] == category2
    mask3 = swim1["Gender"] == "Men"
    mask4 = swim1["Gender"] == "Women"
    swim2 = swim1[mask1 & mask2 & mask3]
    swim3 = swim1[mask1 & mask2 & mask4]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=swim2["Year"], y=swim2["ProcessedTime"], name="Men"))
    fig.add_trace(go.Scatter(x=swim3["Year"], y=swim3["ProcessedTime"], name="Women"))
    st.plotly_chart(fig)