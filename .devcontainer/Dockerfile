FROM mcr.microsoft.com/devcontainers/python:3.10

# Install system dependencies including Java
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    git \
    wget \
    unzip \
    sudo \
    python3-pip \
    python3-dev \
    build-essential \
    openjdk-11-jdk \
    autoconf \
    libtool \
    pkg-config \
    libssl-dev \
    libffi-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$PATH:$JAVA_HOME/bin

# Install Android SDK
ENV ANDROID_HOME=/opt/android-sdk
ENV ANDROID_SDK_ROOT=$ANDROID_HOME
ENV PATH=${PATH}:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools

RUN mkdir -p ${ANDROID_HOME} \
    && wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip \
    && unzip commandlinetools-linux-*_latest.zip -d ${ANDROID_HOME} \
    && rm commandlinetools-linux-*_latest.zip \
    && mkdir -p ${ANDROID_HOME}/cmdline-tools/latest \
    && mv ${ANDROID_HOME}/cmdline-tools/bin ${ANDROID_HOME}/cmdline-tools/latest/ \
    && mv ${ANDROID_HOME}/cmdline-tools/lib ${ANDROID_HOME}/cmdline-tools/latest/ \
    && yes | sdkmanager --licenses \
    && sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.0" "ndk;25.2.9519653"

# Install Buildozer and other Python dependencies
RUN pip3 install --upgrade pip buildozer Cython==0.29.33 kivy[base] pandas openpyxl xlrd

# Set up user permissions
RUN mkdir -p /workspace/.buildozer \
    && chown -R vscode:vscode /workspace/.buildozer \
    && chown -R vscode:vscode ${ANDROID_HOME}

# Verify Java installation
RUN java -version

