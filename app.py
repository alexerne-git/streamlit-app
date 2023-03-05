

from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from PIL import Image
from streamlit_plotly_events import plotly_events
import streamlit as st
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.express as px
import pandas as pd

# Set page configuration
st.set_page_config(page_title="My Streamlit App", page_icon=":smiley:", layout="wide", initial_sidebar_state="expanded")

# Create a file uploader
data = st.file_uploader("Upload a CSV file", type="csv")

    
# If the user uploaded a file
if data is not None:
    data = pd.read_csv(data)
        
    df = pd.DataFrame(data)


    #definition of the interactive plot
    def interactive_plot(dataframe):
        
        #make a dropdown menu for the x and y axis
        x_axis_value =  st.selectbox('Select x-axis', options = dataframe.columns, index= 1)
        st.markdown(
        """
        <style>
        .stSelectbox select {
            width: 200px;
            color:blue;
        }
        .stSelectbox select::-ms-expand {
            width: 20px;
            color:red;
        }
        </style>
        """,
        unsafe_allow_html=True
        )

        y_axis_value =  st.selectbox('Select y-axis', options = dataframe.columns, index= 40)
        

        plot= px.scatter(dataframe, x=x_axis_value, y=y_axis_value, template="plotly_white")
        #st.plotly_chart(plot, use_container_width=True)
        
        plot.update_layout(width=866)

        selected_points = plotly_events(plot, click_event=True, hover_event=False)
        #print selected points
        if not selected_points == []:
            #print pointIndex of selected_points
            id = selected_points[0]['pointIndex']
            
            #locate the id inside the dataframe and print the row
            st.write('Clicked Datapoint:')
            st.write(df.iloc[id])


    html_temp = """
    <div style="background-color:#A8D9FF;padding:1.5px">
    <h1 style="color:black;text-align:center;font-family: 'Roboto', sans-serif;font-weight:400">Project Dashboard </h1>
    </div><br>"""
    st.markdown(html_temp,unsafe_allow_html=True)


    df = pd.DataFrame(data)

    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="single", use_checkbox=True)
    gb.configure_side_bar()
    gridoptions = gb.build()

    custom_css = {
        ".ag-row-hover": {"background-color": "#A8D9FF !important"},
        ".ag-root.ag-unselectable.ag-layout-normal": {"font-size": "16px !important",
    "font-family": "Roboto, sans-serif !important;"},
        ".ag-theme-light button:before": {"content": "'Confirm' !important", "position": "relative !important",
    "z-index": "1000 !important", "top": "0 !important",
    "font-size": "12px !important", "left": "0 !important",
    "padding": "4px !important"}}

    response = AgGrid(
        df,
        height=200,
        gridOptions=gridoptions,
        custom_css=custom_css,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
        header_checkbox_selection_filtered_only=True,
        use_checkbox=True)

    st.write('')
    st.write('')
    st.write('')  

    v = response['selected_rows'] 

    for entry in v:
        
        # Create two columns, each containing a box
        col1, col2,col3 = st.columns([0.47,0.05,0.43])
                    
        with col1:
            default_x_axis = "target_icar"
            default_y_axis = "time_taken"
            
            # Create select boxes for x-axis and y-axis
            x_axis = st.sidebar.selectbox("X-axis", df.columns,index=df.columns.get_loc(default_x_axis))
            y_axis = st.sidebar.selectbox("Y-axis", df.columns,index=df.columns.get_loc(default_y_axis))
            
            # Set the font size and font family using HTML and CSS syntax.
            st.write(f'<div style="background-color: #A8D9FF; padding: 10px;padding-top:19px; margin: 0;width:1000px;"><p style="text-align:center;color: black;font-size: 20pt;width:900px;"> All participants: </p> <span style="font-size: 14pt;"></span><div></div></div>', unsafe_allow_html=True)
            
            # Create scatter plot using selected x-axis and y-axis
            fig = px.scatter(df, x=default_x_axis, y=default_y_axis,color_discrete_sequence=["black"])
            fig.update_layout(width=850,height=600,plot_bgcolor="white")    
            # Display plot
            st.plotly_chart(fig)
                
        with col2:
            st.write("")
    
        with col3:
            def create_polar_line_chart():
                r = [entry["traits_honest"],entry["traits_emoti"],entry["traits_extra"],entry["traits_agree"],entry["traits_consc"],entry["traits_openn"]]
                
                theta = ['Honesty-Humility','Emotionality','Extraversion',
                        'Agreeableness versus Anger', 'Conscientiousness','Openness to Experience']
                fig = go.Figure(data=[go.Scatterpolar(
                                        r=r,
                    
                                        theta=theta,
                                        line_color = "magenta",
                                        marker = dict(
                                            color = "royalblue",
                                            symbol = "square",
                                            size = 8
                                        )
                                        
                                    )],
                                layout=dict(paper_bgcolor='white',
                                            plot_bgcolor='white',
                                            height=500,
                                            margin=dict(l=0, r=0, b=0, t=0)))
                return fig

            div = f"""
                    <div style="background-color:#A8D9FF; padding: 10px;padding-top:19px; margin: 0;width:850px;">
                    <p style="text-align:center;color: black;font-size: 20pt;width:950px;">Personality Traits Scores:</p>
                    </div>
                    <br/>
                    <div></div>
                """
            # Use st.markdown() to display the div
            st.markdown(div, unsafe_allow_html=True)

            # Display the polar line chart using st.plotly_chart()
            fig = create_polar_line_chart()
            fig.update_layout(width=850)  # Set the chart's width to 900 pixels
            st.plotly_chart(fig)
        
    st.write("")
    st.write("")

    v = response['selected_rows'] 

    for entry in v:
        
            # Create two columns, each containing a box
        col1, col2,col3 = st.columns([0.2,0.4,0.5])

        # Display a red box with title and content in the first column
        with col1:
    
            def icar_to_IQ(value):
                if value == '0':
                    return '62'
                elif value == '1':
                    return '62'
                elif value == '2':
                    return '71'
                elif value == '3':
                    return '77'
                elif value == '4':
                    return '83'
                elif value == '5':
                    return '87'
                elif value == '6':
                    return '91'
                elif value == '7':
                    return '94'
                elif value == '8':
                    return '98'
                elif value == '9':
                    return '101' 
                elif value == '10':
                    return '105'
                elif value == '11':
                    return '108'
                elif value == '12':
                    return '112'
                elif value == '13':
                    return '116'
                elif value == '14':
                    return '120'
                elif value == '15':
                    return '124'
                else:
                    return '130'
                    
            st.markdown("<div style='background-color:#A8D9FF;padding:1.5px;padding-top:20px;width:300px;border-radius:5px'> <p style='color:black;text-align:center;font-size:19px'>ICAR:</p>"
        "<p style='color:black;text-align:center;font-size:20px'>{}</p>".format(str(entry["target_icar"])+'</div>'),
        unsafe_allow_html=True)
            
            st.markdown("<div style='background-color:#A8D9FF;padding:1.5px;padding-top:20px;width:300px;border-radius:5px'> <p style='color:black;text-align:center;font-size:19px'>IQ:</p>"
        "<p style='color:black;text-align:center;font-size:20px'>{}</p>".format(icar_to_IQ(str(entry["target_icar"]))+'</div>'),
        unsafe_allow_html=True)
            
            st.markdown("<div style='background-color:#A8D9FF;padding:1.5px;padding-top:20px;width:300px;border-radius:5px'> <p style='color:black;text-align:center;font-size:19px'>Denoised ICAR:</p>"
        "<p style='color:black;text-align:center;font-size:20px'>{}</p>".format(str(round(float(entry["icar_hat0"]),1))+'</div>'),
        unsafe_allow_html=True)

            st.markdown("<div style='background-color:#A8D9FF;padding:1.5px;padding-top:20px;width:300px;border-radius:5px'> <p style='color:black;text-align:center;font-size:19px'>Time taken:</p>"
        "<p style='color:black;text-align:center;font-size:20px'>{}</p>".format(str(round(float(entry["time_taken"]),1))+'</div>'),
        unsafe_allow_html=True)
                    
        with col2:

            video_id_url = 'https://drive.google.com/file/d/1DNb4vXiFBLENkoPKtZeIrtKFpAlQKWfd' # entry["link"]
        
            url = f"{video_id_url}/preview"
            st.write(f'<iframe src="{url}" width="640" height="480"></iframe>', unsafe_allow_html=True)
                    
        with col3:
            first_50_words = ' '.join(entry["text"].split()[:290])
            remaining_text = ' '.join(entry["text"].split()[290:])

            num_words = str(entry["count_word"])
            num_sentences = str(entry["count_sent"])
            # Set the font size and font family using HTML and CSS syntax.
            st.write(f'<div style="background-color: #A8D9FF; padding: 10px;padding-top:19px; margin: 0;width:850px;"><p style="text-align:center;color:black;font-size: 20pt;width:850px;">Participant Transcript: {num_words} words and {num_sentences} sentences</p> <span style="font-size: 14pt;">{first_50_words}</span><div></div></div>', unsafe_allow_html=True)

        # Add a "more" button.
            if st.button('More'):
            
                st.write(f'<div style="background-color: #A8D9FF; padding: 10px;padding-top:19px; margin: 0;width:850px;"><span style="font-size: 14pt;">{remaining_text}</span><div></div></div>', unsafe_allow_html=True)
                
else:
    st.write("Please upload a CSV file.")