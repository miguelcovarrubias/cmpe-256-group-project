# cmpe-256-group-project

### Quick Start for running the Flask App

1: CD to the webapp directory after cloning
```
  $ cd webapp
```

2: Initialize and activate a virtualenv
```
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
```

3: Install the dependencies
```
  $ pip install -r requirements.txt
```


4: Copy the config.py.ex to config.py. In config.py you will put your Spotify API Keys
```
  $ cp config.py.ex config.py
```

5: Run the development server
```
  $ python app.py
```

6: Navigate to [http://127.0.0.1:8080](http://127.0.0.1:8080)
