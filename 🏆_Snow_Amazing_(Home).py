import streamlit as st
import pandas as pd

st.set_page_config(
   page_title="あなたは素晴らしい雪です！バッジ管理",
   page_icon= "🏆"
)

st.image('https://learn.snowflake.com/asset-v1:snowflake+X+X+type@asset+block@snow_amazing_banner.png')

cnx=st.connection("snowflake")
session = cnx.session()
if 'auth_status' not in st.session_state:
   st.session_state['auth_status'] = 'not_authed'
   
def initialize_user_info():
   # session is open but not authed
   st.session_state['auth_status'] = 'not_authed'
   # all profile fields get set back to nothing
   st.session_state['given_name'] = ''
   st.session_state['middle_name'] = ''
   st.session_state['family_name'] = ''
   st.session_state['badge_email'] = ''
   st.session_state['display_name'] = ''
   st.session_state['display_format'] = ''
   st.session_state['display_name_flag'] = 'False'
   # workshop/account fields are set back to nothing 
   st.session_state['workshop_choice'] = '' 
   st.session_state['account_locator'] = ''
   st.session_state['account_identifier'] = ''
   st.session_state['new_record'] = False
   st.session_state['edited_acct_loc'] =''
   st.session_state['edited_acct_id'] =''

def get_user_profile_info():
   #start over with authentication and populating vars
   this_user_sql =  (f"select badge_given_name, badge_middle_name, badge_family_name, display_name, display_format, badge_email "
                     f"from UNI_USER_BADGENAME_BADGEEMAIL where UNI_ID=trim('{st.session_state.uni_id}') "
                     f"and UNI_UUID=trim('{st.session_state.uni_uuid}')")
   this_user_df = session.sql(this_user_sql)
   user_results_pd_df = this_user_df.to_pandas()                          
   user_rows = user_results_pd_df.shape[0]

   if user_rows>=1:
      # if at least one row was found then the key must have been correct so we consider the user authorized
      st.session_state['auth_status'] = 'authed'
       
      # 1 row found means the UNI_ID is legit and can be used to look up other information
      # all user vars need to be checked to make sure they aren't empty before we set session vars
      
      if user_results_pd_df['BADGE_GIVEN_NAME'].iloc[0] is not None:
         st.session_state['given_name'] = user_results_pd_df['BADGE_GIVEN_NAME'].iloc[0]
      
      if user_results_pd_df['BADGE_MIDDLE_NAME'].iloc[0] is not None:    
         st.session_state['middle_name'] = user_results_pd_df['BADGE_MIDDLE_NAME'].iloc[0]
      
      if user_results_pd_df['BADGE_FAMILY_NAME'].iloc[0] is not None:    
         st.session_state['family_name'] = user_results_pd_df['BADGE_FAMILY_NAME'].iloc[0]
      
      if user_results_pd_df['BADGE_EMAIL'].iloc[0] is not None:
         st.session_state['badge_email'] = user_results_pd_df['BADGE_EMAIL'].iloc[0]  
         
      if user_results_pd_df['DISPLAY_NAME'].iloc[0] is not None:
         st.session_state['display_name'] = user_results_pd_df['DISPLAY_NAME'].iloc[0]
         st.session_state['display_name_flag'] = 'True'
      else:
         st.session_state['display_name'] = ":star: ページに移動して、バッジの表示名を生成してください。"
         st.session_state['display_name_flag'] = "False"

      #if user_results_pd_df['display_format'] is not None:
      st.session_state['display_format'] = str(user_results_pd_df['DISPLAY_FORMAT'].iloc[0])
   
   else: # no rows returned
        st.markdown(":red[入力した UNI_ID/UUID の組み合わせの記録はありません。入力ボックスに余分なスペースや改行が含まれていないことを確認してください。また、タブが 15 分以上開いている場合は、ブラウザを更新してみてください。]") 

with st.sidebar:
   st.sidebar.header("User")
   uni_id = st.text_input('learn.snowflake.com UNI ID を入力してください')
   uni_uuid = st.text_input('ワークショップの DORA リスニング ページに表示されるシークレット UUID を入力します。')
   find_my_uni_record = st.button("UNI ユーザー情報を探す")
   # st.session_state

# Page Header
st.header('あなたは素晴らしい雪です')
st.write('learn.snowflake.com ワークショップ バッジ管理アプリへようこそ!')
st.write('このアプリを使用すると、バッジの名前と電子メールを管理し、結果を表示できます。')


if find_my_uni_record:
   # reset all session vars
   initialize_user_info()
  

   # Set uni_id and key to entries on form
   st.session_state['uni_id'] = uni_id
   st.session_state['uni_uuid'] = uni_uuid


   # this will query the db and if finds a match will populate profile vars
   get_user_profile_info()
   

if st.session_state.auth_status == 'authed':
   # st.write(st.session_state.display_format)
   st.subheader("We Found You!")
   st.markdown("**名:** " + st.session_state.given_name)
   st.markdown("**ミドルネーム/別名:** "+ st.session_state.middle_name) 
   st.markdown("**苗字:** " + st.session_state.family_name)
   st.markdown("**Eメール:** " + st.session_state.badge_email)
   if st.session_state.display_name_flag != "False":
      st.markdown("**名前はバッジに次のように表示されます。:** :green[" + st.session_state.display_name + "]")
   else:
      md_str =  "**名前はバッジに次のように表示されます。:** :red[" + st.session_state.display_name + "]"       
      st.markdown(md_str)
      st.write("-----")
      st.markdown("*表示名が生成されていない場合、または名前、メールアドレス、表示名を変更したい場合は、✏️ ページに移動して編集してください。*")
else:
   st.markdown(":red[サイドバーで UNI_ID と UUID を使用してサインインしてください。]")
