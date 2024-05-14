import torch
from torchvision import models, transforms
import json 

num_classes = 3
cv_model = models.resnet18()
transformations = transforms.Compose([
transforms.Resize(256),
transforms.CenterCrop(400),
transforms.ToTensor(),
transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])

# weights = torch.load('models/model_multiclass.pt')
weights = torch.load('models/model_finetuning_experiment2.pt')
new_classifier = torch.nn.Sequential(
    torch.nn.Linear(in_features=512, out_features=num_classes),
    torch.nn.Softmax() 
)
cv_model.fc = new_classifier
cv_model.load_state_dict(weights)
cv_model.eval()
with open('models/idx_to_class.json', 'r') as f:
    temp = json.load(f)

idx_to_class = {}
for key, value in temp.items():
    idx_to_class[int(key)] = value
