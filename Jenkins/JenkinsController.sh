#!/bin/bash

JENKINS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
JENKINS_HOME="$JENKINS_DIR/workspace"
JENKINS_PORT=8080

export JENKINS_HOME=$JENKINS_HOME

if [ ! -f "$JENKINS_DIR/jenkins.war" ]; then
  curl -L "https://updates.jenkins.io/latest/jenkins.war" -o "$JENKINS_DIR"/jenkins.war
fi

java -jar "$JENKINS_DIR"/jenkins.war &

sleep 45

if [ -f "$JENKINS_HOME/secrets/initialAdminPassword" ]; then
  adminPw=$(cat "$JENKINS_HOME/secrets/initialAdminPassword")
  echo "Admin password: $adminPw"
else
  echo "Error: initialAdminPassword file not found"
fi

echo "Initializing plugin installation..."

if [ -f "jenkins.yaml" ]; then
  mv jenkins.yaml "$JENKINS_HOME/jenkins.yaml"
fi

if [ ! -f "$JENKINS_DIR/jenkins-cli.jar" ]; then
  curl -L "http://localhost:$JENKINS_PORT/jnlpJars/jenkins-cli.jar" -o "$JENKINS_DIR/jenkins-cli.jar"
fi

java -jar "$JENKINS_DIR/jenkins-cli.jar" -s "http://localhost:$JENKINS_PORT" -auth "admin:$adminPw" who-am-i

if [ -f "$JENKINS_DIR/plugins.txt" ]; then
  PLUGINS=(
    "configuration-as-code:1807.v0175eda_00a_20"
    "pipeline-stage-view:2.34"
    "job-dsl:1.87"
    "cloudbees-folder:6.940.v7fa_03b_f14759"
    "branch-api:2.1169.va_f810c56e895"
    "workflow-aggregator:596.v8c21c963d92d"
    "workflow-multibranch:791.v28fb_f74dfca_e"
    "workflow-job:1415.v4f9c9131248b_"
    "groovy:457.v99900cb_85593"
    "git:5.2.2"
    "github:1.39.0"
  )
  for plugin in "${PLUGINS[@]}"; do
    java -jar "$JENKINS_DIR/jenkins-cli.jar" -s "http://localhost:$JENKINS_PORT/" -auth "admin:$adminPw" install-plugin "$plugin"
  done
fi

echo "Restarting Jenkins to make plugins usable..."
java -jar jenkins-cli.jar -s http://localhost:8080/ -auth "admin:$adminPw" safe-restart
