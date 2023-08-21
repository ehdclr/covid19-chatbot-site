from flask import Flask, render_template, Response
import corona_data
from datetime import date, timedelta
import requests

# 앱 생성
app = Flask(__name__)


# url 라우터
@app.route('/')
def index():
    now = date.today()
    now_str = now.strftime("%Y%m%d")
    print(now_str)

    # 오늘날짜로 요청해라
    data = corona_data.get_corona_data(now_str, now_str)
    print(data)

    # 없으면 어제 날짜로 요청해라
    if not data:
        yesterday = now - timedelta(days=1)
        yesterday_str = yesterday.strftime("%Y%m%d")
        print(yesterday_str)

        data = corona_data.get_corona_data(yesterday_str, yesterday_str)
        print(data)

    return render_template('dd.html', data1=data[:1], data=data[1:], image_file="img/per.jpg", image_file1="img/vac.jpg")



# 메인 영역
if __name__ == "__main__":
    app.run(debug=True)
