# AI Smart Assistant - Face Authentication + Voice/Text Command Execution

## 🎯 Project Overview

An intelligent desktop assistant that combines **face authentication** with **voice and text commands** to execute various system tasks. Built with Python, this application provides secure access through facial recognition and allows users to control their computer using natural language commands.

## ✨ Features

### 1. Face Authentication Module
- **Face Detection** using Haar Cascade
- **Face Recognition** using face_recognition library
- **User Registration** with 20 face samples for accuracy
- **Real-time Authentication** via webcam
- **Visual Feedback** with bounding boxes and user names

### 2. Voice Command Module
- **Speech Recognition** using Google Speech API
- **Microphone Input** with ambient noise adjustment
- **Text-to-Speech** responses using pyttsx3
- **Error Handling** for unclear speech

### 3. Text Command Module
- **Command-line Interface** for text input
- **Continuous Command Loop**
- **Help System** for available commands

### 4. Intelligent Command Execution
- **Application Launcher**: Calculator, Notepad, Chrome
- **Web Shortcuts**: YouTube, Google
- **System Information**: Current time and date
- **Voice Feedback** for executed commands

## 📋 Requirements

### Hardware Requirements
- Webcam (for face authentication)
- Microphone (for voice commands)
- Windows OS (tested on Windows 10/11)

### Software Requirements
- Python 3.8 or higher
- VS Code or any Python IDE

## 🔧 Installation Guide

### Step 1: Install Python
Download and install Python 3.8+ from [python.org](https://python.org)

### Step 2: Create Project Directory
```bash
mkdir AI_Capstone
cd AI_Capstone
