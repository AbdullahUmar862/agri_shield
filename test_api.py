import requests

url = "http://127.0.0.1:5000/api/analyze_fruit"
files = {'image': open(r"C:\venv\project_fruit_dataset\train\Mango_Healthy\1.jpg", 'rb')}

response = requests.post(url, files=files)
print(response.json())
