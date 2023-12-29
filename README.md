# Reddit_Text_to_Video
Python code that extracts subreddit stories and turn it into a video

### Get a reddit client_id, client_secret and find out your user_agent(i.e. web browser name)
Follow this link to get your <b>client_id</b> and <b>client_secret</b>
> [https://github.com/reddit-archive/reddit/wiki/OAuth2](https://github.com/reddit-archive/reddit/wiki/OAuth2)

How to find out your <b>user_agent</b>
![image](https://github.com/shaeka/Reddit_Text_to_Video/assets/56749928/7a8432cb-0f42-4766-85fc-4fb945293235)

### How to use this script
1. Download the file
2. Extract the zip file
3. Open up notepad, key in the following details and save the file as .env inside the extracted folder
```
client_id="YOUR_CLIENT_ID"
client_secret="YOUR_CLIENT_SECRET"
user_agent="YOUR_USER_AGENT"
```
4. Open up anaconda prompt or command prompt and activate anaconda environment
5. Create a new conda environment
```
conda create --name new_env python==3.10
```
6. Activate the environment
```
conda activate new_env
```
7. Change directory to the location of the extracted folder (e.g. in Downloads)
```
cd C:/Users/enter_your_user/Downloads/extracted_filename
```
8. Install the required libraries
```
pip install -r requirements.txt
```
9. Run the code
```
python reddit_text_to_video.py
```
