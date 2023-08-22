import cv2
import numpy as np
import torch
from openvino.preprocess import PrePostProcessor, ResizeAlgorithm
from openvino.runtime import Core, Layout, Type
from torchvision import transforms as T
from PIL import Image 
from torchvision.utils import save_image

class ganimation(object):
    def __init__(self,image):
        #image = cv2.imread(r"C:\openvino-workspace\ganimation-master\ganimation-master\animations\eric_andre\ganimation_IR\capture_image\test1.jpg")
        self.image = image
        
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.core = Core()
        self.model = self.core.read_model("./ganimation.xml")
        self.csv_lines = open("./attr.txt", 'r').readlines()

        self.regular_image_transform = []
        self.regular_image_transform.append(T.ToTensor())
        self.regular_image_transform.append(T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)))
        self.regular_image_transform = T.Compose(self.regular_image_transform)

    def produce_pics(self):
        test_tensor = self.regular_image_transform(self.image)
      
        test_nparray = test_tensor.numpy().astype(np.float32)
        images=[]
        print('生成中...')
        for i in range(16):
          images.append(test_nparray)
        images=np.array(images)

        targets = torch.zeros(len(self.csv_lines), 17)

        for idx, line in enumerate(self.csv_lines):
            splitted_lines = line.split(' ')
            targets[idx, :] = torch.Tensor(np.array(list(map(lambda x: float(x)/5., splitted_lines[1::]))))
        targets = targets.numpy()

        # Inference
        #model = ppp.build()
        compiled_model = self.core.compile_model(self.model, "AUTO")
        results = compiled_model.infer_new_request({0: images, 1: targets[:16]})
        reg = list(results.values())[1]
        attr = list(results.values())[0]

        output = self.imFromAttReg(att=attr, reg=reg, x_real=images)
        output = (output+1)/2
        output_Tensor = torch.Tensor(output)
        for i in range(output_Tensor.shape[0]):
          save_image(output_Tensor[i].unsqueeze(0), "result/hannibal_{}.jpg".format(i))
        print('完成')
        return output

    def imFromAttReg(self, att, reg, x_real):
              #Mixes attention, color and real images
              return (1-att)*reg + att*x_real
"""

core = Core()
model = core.read_model(r"C:\openvino-workspace\ganimation-master\ganimation-master\animations\eric_andre\ganimation_IR\ganimation.xml")
image = cv2.imread(r"C:\openvino-workspace\ganimation-master\ganimation-master\animations\eric_andre\ganimation_IR\capture_image\input_img.jpg")
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
csv_lines = open(r"C:\openvino-workspace\ganimation-master\ganimation-master\animations\eric_andre\ganimation_IR\attr.txt", 'r').readlines()
input_tensor = np.expand_dims(image, 0)

regular_image_transform = []
regular_image_transform.append(T.ToTensor())
regular_image_transform.append(T.Normalize(mean=(0.5, 0.5, 0.5), std=(0.5, 0.5, 0.5)))
regular_image_transform = T.Compose(regular_image_transform)

'''
ppp = PrePostProcessor(model)
_, h, w, _ = 16,1170,1170,3
ppp.input(0).tensor().set_element_type(Type.f32).set_layout(Layout("NCHW")).set_spatial_static_shape(h, w)
ppp.input(0).preprocess().resize(ResizeAlgorithm.RESIZE_LINEAR,128,128)
ppp.input(0).model().set_layout(Layout("NCHW"))
ppp.output(0).tensor().set_element_type(Type.f32)
ppp.output(1).tensor().set_element_type(Type.f32)
'''

#image = Image.open(r"C:\openvino-workspace\ganimation-master\ganimation-master\animations\eric_andre\ganimation_IR\capture_image\test.jpg")

test_tensor = regular_image_transform(image)

test_nparray = test_tensor.numpy().astype(np.float32)
images=[]
print('生成中...')
for i in range(16):
  images.append(test_nparray)
images=np.array(images)

targets = torch.zeros(len(csv_lines), 17)

for idx, line in enumerate(csv_lines):
    splitted_lines = line.split(' ')
    targets[idx, :] = torch.Tensor(np.array(list(map(lambda x: float(x)/5., splitted_lines[1::]))))
targets = targets.numpy()

# Inference
#model = ppp.build()
compiled_model = core.compile_model(model, "AUTO")
results = compiled_model.infer_new_request({0: images, 1: targets[:16]})
reg = list(results.values())[1]
attr = list(results.values())[0]
def imFromAttReg(att, reg, x_real):
        #Mixes attention, color and real images
        return (1-att)*reg + att*x_real

output = imFromAttReg(att=attr, reg=reg, x_real=images)
output = (output+1)/2
output = torch.Tensor(output)
for i in range(output.shape[0]):
  save_image(output[i].unsqueeze(0), "result/hannibal_{}.jpg".format(i))


"""
