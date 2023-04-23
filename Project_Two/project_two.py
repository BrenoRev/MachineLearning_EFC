# -*- coding: utf-8 -*-
"""Project_Two

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u7azOsz-zpHFOBJnKS14K-C1TukkQGJS

### Classification of Cars with Machine Learning
"""

# This code installs and sets up the fastbook library as a dependency.

! [ -e /content ] && pip install -Uqq fastbook
import fastbook
fastbook.setup_book()

# Import dependencies

from fastbook import *
from fastai.vision.widgets import *

# Setting key

key = os.environ.get('AZURE_SEARCH_KEY', '74f7dde4575e4799800cae9dbb7d6e6f')

# Search Images

search_images_bing

# Search image of real cars

results = search_images_bing(key, 'carros')
ims = results.attrgot('contentUrl')
len(ims)

# Getting image from yellow car

ims = ['https://images.cdn.circlesix.co/image/1/640/0/uploads/articles/dsc_2049_60809-564c6f63611b8.jpg']

# Save the image

dest = 'images/yellow_car.jpg'
download_url(ims[0], dest)

# Open and show the image

im = Image.open(dest)
im.to_thumb(256,256)

# Setting avaliables car colors

cars_colors = 'black','white','blue', 'yellow','green'
path = Path('carros')

# Get image from each cars_colors and download it

if not path.exists():
    path.mkdir()
    for o in cars_colors:
        dest = (path/o)
        dest.mkdir(exist_ok=True)
        results = search_images_bing(key, f'{o} carros')
        download_images(dest, urls=results.attrgot('contentUrl'))

# Gets all the image files within the specified directory path and assigns them to the variable fns

fns = get_image_files(path)
fns

# Prepare the data for training a model on images of cars

cars = DataBlock(
    blocks=(ImageBlock, CategoryBlock), 
    get_items=get_image_files, 
    splitter=RandomSplitter(valid_pct=0.2, seed=42),
    get_y=parent_label,
    item_tfms=Resize(128))

# This code creates a dataloader object dls from the cars DataBlock using the path specified earlier as the source of the data.

dls = cars.dataloaders(path)

# Will display a batch of images from the validation set of the dataloaders object created from the cars DataBlock.

dls.valid.show_batch()

# This code block resizes the images in the cars datablock to a fixed size of 128 pixels using the Resize transformation with ResizeMethod.Squish parameter
# creates a new dataloader with the resized images, and displays a batch of 4 unique images from the validation set with a maximum of 1 row.

cars = cars.new(item_tfms=Resize(128, ResizeMethod.Squish))
dls = cars.dataloaders(path)
dls.valid.show_batch(max_n=4, nrows=1, unique=True)

# Resizes the images to have a height and width of 64 pixels using padding to maintain the aspect ratio of the images
# and sets the padding mode to 'zeros'. Then it creates a new dataloader object based on the modified dataset and shows a batch of four validation images in one row.

cars = cars.new(item_tfms=Resize(64, ResizeMethod.Pad, pad_mode='zeros'))
dls = cars.dataloaders(path)
dls.valid.show_batch(max_n=5, nrows=3)

# This code randomly crops images in the training set using RandomResizedCrop with a minimum scale of 0.89 and displays a batch of 4 unique images in a single row.

cars = cars.new(item_tfms=RandomResizedCrop(224, min_scale=0.89))
dls = cars.dataloaders(path)
dls.train.show_batch(max_n=10, nrows=2, unique=True)

# This code sets up a convolutional neural network using the ResNet18 architecture
# and fine-tunes it on the given dataloaders for 4 epochs. The performance of the model is evaluated using the error_rate metric.
learn = cnn_learner(dls, resnet18, metrics=error_rate)
learn.fine_tune(4)

# The code creates a convolutional neural network learner object learn using a ResNet34 model architecture and the dataloaders dls.
# It then fine-tunes the pre-trained model for 4 epochs with a base learning rate of 0.1, using the fine_tune() method. The metric used to evaluate the model is the error rate.

learn = cnn_learner(dls, resnet34, metrics=error_rate)
learn.fine_tune(4, base_lr= 0.1)

# The code defines a cnn_learner object with a ResNet34 architecture and the error_rate metric.
# it then calls the fine_tune method to train the model for 4 epochs with a default learning rate.

learn = cnn_learner(dls, resnet34, metrics=error_rate)
md = learn.lr_find(suggest_funcs=(minimum, steep))

# Print

print(f"Minimum/10: {md.minimum:.2e}, steepest point: {md.steep:.2e}")

# creates an instance of the ClassificationInterpretation class from the cnn_learner model
# and uses it to plot a confusion matrix, which is a visual representation of the performance of the model in classifying the validation set
# showing the number of true positive, false positive, true negative, and false negative predictions for each class.

interp = ClassificationInterpretation.from_learner(learn)
interp.plot_confusion_matrix()

#  generates a plot of the top losses in the validation set, showing the image with highest loss, 
# the predicted label and the true label. In this case, the plot shows the top 3 losses, with all images in the same row.

interp.plot_top_losses(3, nrows=1)

# Creates an instance of the ImageClassifierCleaner class with the specified model.

cleaner = ImageClassifierCleaner(learn)
cleaner

"""### Deploy"""

# Export

learn.export()

# Export the file

path = Path()
path.ls(file_exts='.pkl')

# Load model

learn_inf = load_learner(path/'export.pkl')

# Chance

learn_inf.predict('images/yellow_car.jpg')

# Options

learn_inf.dls.vocab

# The code creates a button to upload an image file, a button to classify the image, an output widget to display the image
# and a label widget to show the prediction and probability of the classification.
# The on_click_classify function is called when the classify button is clicked, which reads the uploaded image
# displays it in the output widget, and performs a prediction using the trained model, which is then displayed in the label widget.

btn_upload = widgets.FileUpload()
btn_run = widgets.Button(description='Classify')
out_pl = widgets.Output()
lbl_pred = widgets.Label()

def on_click_classify(change):
    img = PILImage.create(btn_upload.data[-1])
    out_pl.clear_output()
    with out_pl: display(img.to_thumb(128,128))
    pred,pred_idx,probs = model_inf.predict(img)
    lbl_pred.value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'
    
btn_run.on_click(on_click_classify)

# Fake the image

btn_upload = SimpleNamespace(data = ['images/yellow_car.jpg'])

# Create

img = PILImage.create(btn_upload.data[-1])

# out_pl is an Output widget that can be used to display output from other widgets.
# Here, the code is clearing the output and displaying the thumbnail of an image of size 256x256 in the out_pl widget.
# However, since there is no image variable defined in this code, it will throw an error.

out_pl = widgets.Output()
out_pl.clear_output()
with out_pl: display(img.to_thumb(256,256))
out_pl

# This line of code uses the predict method of a learner object to make predictions on an input image

pred,pred_idx,probs = learn_inf.predict(img)

# The code creates a label widget and sets its value to a string containing the predicted label and probability for an image classification task.

lbl_pred = widgets.Label()
lbl_pred.value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'
lbl_pred

# Run the classify

btn_run = widgets.Button(description='Classify')
btn_run

# Classify function
def on_click_classify(change):
    img = PILImage.create(btn_upload.data[-1])
    out_pl.clear_output()
    with out_pl: display(img.to_thumb(128,128))
    pred,pred_idx,probs = learn_inf.predict(img)
    lbl_pred.value = f'Prediction: {pred}; Probability: {probs[pred_idx]:.04f}'

btn_run.on_click(on_click_classify)

# Widget of file upload

btn_upload = widgets.FileUpload()

# Widget showing the chance
VBox([widgets.Label('Select the car from your computer'), 
      btn_upload, btn_run, out_pl, lbl_pred])

from google.colab import drive
drive.mount('/content/drive')