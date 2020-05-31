# Info

I've used yaml to store some keyword and value for my bot. But as it is hard to maintain I want to rebuild the storing way. And this program is written for quickly transferring all key and value to mysql tables. 

~~Actually not so quick cuz i've build this program for 2 days~~  

**Only for simple yaml structure**

# Usage

- Put YAML file into venv package

- Create a `cfg.yml` file and put db info in it:

```yaml
host: localhost
user: root
password: 123456
``` 

- Open bash and install dependence.

```bash
pip3 install pyyaml mysql-connector-python -i https://pypi.tuna.tsinghua.edu.cn/simple
``` 

- RUN

```bash
python3 ./venv/YAML2MYSQL.py
```

