from flask import Flask, render_template, request
import numpy as np
import os
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

from sklearn.metrics import accuracy_score

filepath = r'C:\Users\Pabitra\Downloads\plant_disease_prediction_using_CNN-main\model.h5'
model = load_model(filepath)
print(model)

print("Model Loaded Successfully")

def pred_tomato_dieas(tomato_plant):
  test_image = load_img(tomato_plant, target_size = (128, 128)) # load image 
  print("@@ Got Image for prediction")  #step 3
  
  test_image = img_to_array(test_image)/255 # convert image to array and normalize
  test_image = np.expand_dims(test_image, axis = 0) 
  
  result = model.predict(test_image) # predict diseased plant or not
  print('@@ Raw result = ', result)  #step 4
  
  pred = np.argmax(result, axis=1)
  print(pred)
  if pred==0:
      return "Leaf - Bacteria Spot Disease", 'Tomato-Bacteria Spot.html'
       
  elif pred==1:
      return "Tomato - Early Blight Disease", 'Tomato-Early_Blight.html'
        
  elif pred==2:
      return "Tomato - Healthy and Fresh", 'Tomato-Healthy.html'
        
  elif pred==3:
      return "Tomato - Late Blight Disease", 'Tomato - Late_blight.html'
       
  elif pred==4:
      return "Tomato - Leaf Mold Disease", 'Tomato - Leaf_Mold.html'
        
  elif pred==5:
      return "Tomato - Septoria Leaf Spot Disease", 'Tomato - Septoria_leaf_spot.html'
        
  elif pred==6:
      return "Tomato - Target Spot Disease", 'Tomato - Target_Spot.html'
        
  elif pred==7:
      return "Tomato - Tomoato Yellow Leaf Curl Virus Disease", 'Tomato - Tomato_Yellow_Leaf_Curl_Virus.html'
 
  elif pred==8:
      return "Tomato - Tomato Mosaic Virus Disease", 'Tomato - Tomato_mosaic_virus.html'
        
  elif pred==9:
      return "Tomato - Two Spotted Spider Mite Disease", 'Tomato - Two-spotted_spider_mite.html'


# score=accuracy_score(y,y_pred)

# score=accuracy_score(pred_tomato_dieas)
# print(score)

def get_true_label(filename):
    label = filename.split('_')[0]
    return label

def calculate_accuracy():
    test_dir = r'C:\Users\Pabitra\Downloads\plant_disease_prediction_using_CNN-main\Dataset\test'  # Set the path to the directory containing test images
    
    test_images = os.listdir(test_dir)  # Get the list of test images
    
    total_images = len(test_images)
    correct_predictions = 0
    
    for image_name in test_images:
        image_path = os.path.join(test_dir, image_name)
        result, _ = pred_tomato_dieas(image_path)
        
        true_label = get_true_label(image_name)  # Get the true label from the image filename or metadata
        
        if result == true_label:  # Check if the predicted label matches the true label
            correct_predictions += 1
    
    accuracy = (correct_predictions / total_images) * 100
    print("Accuracy: {:.2f}%".format(accuracy))
    return(accuracy)


# Create flask instance
app = Flask(__name__)

# render index.html page
@app.route("/", methods=['GET', 'POST'])
def home():
        return render_template('index.html')

# get input image from client then predict class and render respective .html page for solution
@app.route("/predict", methods = ['GET','POST'])
def predict():
     if request.method == 'POST':
        file = request.files['image'] 
        filename = file.filename        
        print("@@ Input posted = ", filename)  #step 1
        
        file_path = os.path.join(r'C:\Users\Pabitra\Downloads\plant_disease_prediction_using_CNN-main\static\upload', filename)
        file.save(file_path)

        print("@@ Predicting class......")  #step 2
        pred, output_page = pred_tomato_dieas(tomato_plant=file_path)
        accuracy = calculate_accuracy()      
        return render_template(output_page,accuracy = accuracy, pred_output = pred, user_image = file_path)

# For local system & cloud    
if __name__ == "__main__":
    app.run(threaded=False,port=8080) 
    
    
