import subprocess
import json
import os

NF_CONFIG = {
    "IMAGE_AMF": "free5gc/amf:v1.2.5",
    "K8S_NAMESPACE": "free5gc",
    "K8S_POD_AMF": "amf-0"
}