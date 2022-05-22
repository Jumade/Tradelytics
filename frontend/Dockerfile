FROM node:16

# Create app directory
WORKDIR /usr/src/tradelytics

ENV PATH /usr/src/tradelytics/node_modules/.bin:$PATH

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
#RUN npm install react-scripts@5.0.0 -g --silent
# If you are building your code for production
# RUN npm ci --only=production

# Bundle app source
COPY . .

CMD [ "npm", "start" ]