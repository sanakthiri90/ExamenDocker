import json
import json
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import librosa.display
import librosa 
import numpy as np
import pickle

