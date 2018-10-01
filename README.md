# Pseudo automated code review

This repo is a usefull helper to do a security code review on a big project.

## Launch

```bash
git clone https://github.com/HugoDelval/pseudo-automated-code-review && cd pseudo-automated-code-review 
vim projects # 1 git project/line : [name of your project][space][git url of your project]\n
python3 extract_bad_practices.py
```

Outputs are writen in *outputs.json*.

Please look at config.py for customization. 

## Add a plugin

### Write the plugin in code_review_plugins

```bash
cp code_review_plugins/python.py your_language/python.py
vim your_language/python.py
```

Write your plugin with the method you like, my plugins are based on the Unix utilities **find** and **grep** but you can do whatever you want. 

The method **launch_code_review()** is where you can to write your code. 

### Update config

```bash
vim config.py
```

Add a constant on top of the file (ex: *PHP = 8*). And add it to the dict **languages**.

### Automatically detect language when cloning repo


```bash
vim extract_bad_practices.py
```

You can update the method **detect_language** by adding your custom language detection, based on the parameter **custom_repo_path**. I based my detection on the Unix utility **find**.

Just write a line before the maximum_score calculus:

```python3
scores['php'] = ( NUMBER_OF_PHP_FILES , config.PHP)
maximum_score = ...
```

And you are good to go! :)
