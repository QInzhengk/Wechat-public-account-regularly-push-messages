# 微信公众号定时推送消息

![GitHub repo size](https://img.shields.io/github/repo-size/QInzhengk/the_milky_way?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/QInzhengk/the_milky_way?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/QInzhengk/the_milky_way?style=for-the-badge)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/QInzhengk/the_milky_way?style=for-the-badge)
![Bitbucket issues](https://img.shields.io/github/issues-closed/QInzhengk/the_milky_way?style=for-the-badge)

## 📒 简介

> :smiley: 通过GitHub Actions给微信公众测试号定时推送消息（Python）。

## 🤝 [博客](https://github.com/qzkq/qzkq.github.io)

[the_milky_way](https://qzkq.github.io/)

## [https://github.com/QInzhengk/Math-Model-and-Machine-Learning](https://github.com/QInzhengk/Math-Model-and-Machine-Learning)
## 简介
GitHub Actions 是 GitHub 推出的持续集成服务。

> 在 GitHub Actions 的仓库中自动化、自定义和执行软件开发工作流程。 您可以发现、创建和共享操作以执行您喜欢的任何作业（包括 CI/CD），并将操作合并到完全自定义的工作流程中。

就是你可以给你的代码仓库部署一系列自动化脚本，在你进行了提交/合并分支等操作后，自动执行脚本。
## GitHub Actions 术语

 - workflow （工作流程）：持续集成一次运行的过程，就是一个 workflow。
 -  job （任务）：一个 workflow由一个或多个 jobs 构成，含义是一次持续集成的运行，可以完成多个任务。
 -  step（步骤）：每个 job 由多个 step构成，一步步完成。 
 - action （动作）：每个 step 可以依次执行一个或多个命令（action）。

### workflow 文件
GitHub Actions 的配置文件叫做 workflow 文件，存放在代码仓库的.github/workflows目录。

workflow 文件采用 YAML 格式，文件名可以任意取，但是后缀名统一为.yml，默认为main.yml。一个库可以有多个 workflow 文件。GitHub 只要发现.github/workflows目录里面有.yml文件，就会自动运行该文件。
#### 1.name
workflow的名称。如果省略该字段，默认为当前workflow的文件名。
#### 2.on
触发workflow的条件，通常是某些事件，详细内容可以参照 [官方文档](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) 。
例

```python
on: push
```

上面代码指定，push事件触发 workflow。

on字段也可以是事件的数组。


```python
on: [push, pull_request]
```

上面代码指定，push事件或pull_request事件都可以触发 workflow。

除了代码库事件，GitHub Actions 也支持外部事件触发，或者定时运行。

```python
on.<push|pull_request>.<tags|branches>
```

指定触发事件时，可以限定分支或标签。

```python
on:
  push:
    branches:    
      - master
```

上面代码指定，只有master分支发生push事件时，才会触发 workflow。

```python
on.schedule
```
后续定时推送微信公众测试号需要设置的；预定的工作流程在默认或基础分支的最新提交上运行。您可以运行预定工作流程的最短间隔是每 5 分钟一次。

在每天 5：30 和 17：30 UTC 触发工作流程（注意utc时间和中国时间差异）：

```python
on:
  schedule:
    # * is a special character in YAML so you have to quote this string
    - cron:  '30 5,17 * * *'
```
多个 事件可以触发单个工作流。你可以通过 上下文访问触发工作流的计划事件。此示例触发工作流在每周一至周四 5：30 UTC 运行，但在周一和周三跳过 步骤。

```python
on:
  schedule:
    - cron: '30 5 * * 1,3'
    - cron: '30 5 * * 2,4'

jobs:
  test_schedule:
    runs-on: ubuntu-latest
    steps:
      - name: Not on Monday or Wednesday
        if: github.event.schedule != '30 5 * * 1,3'
        run: echo "This step will be skipped on Monday and Wednesday"
      - name: Every time
        run: echo "This step will always run"
```

#### 3.jobs

```python
jobs.<job_id>.name
```

workflow 文件的主体是jobs字段，表示要执行的一项或多项任务。

jobs字段里面，需要写出每一项任务的job_id，具体名称自定义。job_id里面的name字段是任务的说明。

```python
jobs:
  my_first_job:
    name: My first job
  my_second_job:
    name: My second job
```

上面代码的jobs字段包含两项任务，job_id分别是my_first_job和my_second_job。

```python
jobs.<job_id>.needs
```

needs字段指定当前任务的依赖关系，即运行顺序。

```python
jobs:
  job1:
  job2:
    needs: job1
  job3:
    needs: [job1, job2]
```

上面代码中，job1必须先于job2完成，而job3等待job1和job2的完成才能运行。因此，这个 workflow 的运行顺序依次为：job1、job2、job3。

```python
jobs.<job_id>.runs-on
```

runs-on字段指定运行所需要的虚拟机环境。它是必填字段。目前可用的虚拟机如下：

 - **ubuntu-lates**t，ubuntu-22.04或ubuntu-20.04
 -  **windows-latest**，windows-2022或windows-2019
 -  **macOS-latest**，macOS-12或macOS-11

指定虚拟机环境为ubuntu-20.04

```python
runs-on: ubuntu-20.04
```


```python
jobs.<job_id>.steps
```

steps字段指定每个 Job 的运行步骤，可以包含一个或多个步骤。每个步骤都可以指定以下三个字段。

 - jobs.<job_id>.steps.name：步骤名称。 
 - jobs.<job_id>.steps.run：该步骤运行的命令或者 action。 
 - jobs.<job_id>.steps.env：该步骤所需的环境变量。

### 几个完整的 workflow 文件的范例
#### 一
```python
#工作名字
name: qin
#
on:
  workflow_dispatch: 
  push:
  # 当对分支master进行push操作的时候，这个工作流就被触发了
    branches: [ master ]
  pull_request:
  #只运行特定分支master
    branches: [ master ]
  schedule:
  # 定时任务，在每天的24点 18点推送签到信息到邮箱
    - cron:  0 16 * * * 
  #watch:
  #    types: started   

jobs:
#将工作流程中运行的所有作业组合在一起
  kai:
  #定义名为 kai 的作业。 子键将定义作业的属性 
    runs-on: ubuntu-latest
    #将作业配置为在最新版本的 Ubuntu Linux 运行器上运行
    #if: github.event.repository.owner.id == github.event.sender.id
    # https://p3terx.com/archives/github-actions-manual-trigger.html
    
    steps:
    - uses: actions/checkout@v2
#uses 关键字指定此步骤将运行 actions/checkout 操作的 v3。 这是一个将存储
#库签出到运行器上的操作，允许您对代码（如生成和测试工具）运行脚本或其他操
#作。 每当工作流程将针对存储库的代码运行时，都应使用签出操作。
    
    - name: Set up Python 3.9
      uses: actions/setup-python@v2
      with:
        python-version: 3.9.1
    - name: requirements
      run: |
        python -m pip install --upgrade pip
        pip3 install -r requirements.txt
       # if [ -f requirements.txt ]; then pip install -r requirements.txt; fi 
    - name: Checkin
      run: |
        python3 ./test.py 
  env: 
  #设置secrets的环境变量
    COOKIE1: ${{ secrets.COOKIE1 }}
    COOKIE2: ${{ secrets.COOKIE2 }}
    #SMTP: ${{ secrets.SMTP }}
    MAIL1: ${{ secrets.MAIL1 }}
    MAIL2: ${{ secrets.MAIL2 }}
```
#### 二

```python
name: Schedule Worker
on:
  schedule:
    - cron: '40 3,9 * * *' #每日11点40,17点40，两个时间点执行任务
jobs:
  work:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: szenius/set-timezone@v1.0 # 设置执行环境的时区
        with:
          timezoneLinux: "Asia/Shanghai"
      - uses: actions/setup-python@v4 # 使用python装配器
        with:
          python-version: '3.10' # 指定python版本
          cache: 'poetry' # 设置缓存

      - run: poetry install --without dev # 安装
      - run: poetry run python .\bin.py # 执行
```
## 实例1、通过GitHub Actions给微信公众测试号定时推送消息（Python）
### 1、微信公众号步骤
打开 微信公众测试平台 ，通过微信扫一扫登录注册一个测试号。

**APP_ID**、**APP_SECRET**（复制自己的appID和appsecret）
![在这里插入图片描述](https://img-blog.csdnimg.cn/ee6a62241c1d41628ddcb0ef2dca89f2.png)
**USER_ID**（复制关注测试号的用户微信号，可以给多个用户推送）
![在这里插入图片描述](https://img-blog.csdnimg.cn/710585c11f054b1d91cd198bc186ea71.png)
自己新增测试模板（可根据自己喜好修改）
![在这里插入图片描述](https://img-blog.csdnimg.cn/66495a10fcda41b7a0e80b6e3b478dee.png)

**TEMPLATE_ID**（模板ID）
![在这里插入图片描述](https://img-blog.csdnimg.cn/c1483cf48d6a44ae8e6a457b1adc0fe9.png)
### 2、github步骤

新建或选取一个自己的公开库（也可以直接fork别人写好的），点击**Actions**，选择**New workflow**
![在这里插入图片描述](https://img-blog.csdnimg.cn/094b0eee40a24fd8a0a1de9b5c550cb4.png)
选择**set up a workflow yourself**，也可以搜索现成的wordflow
![在这里插入图片描述](https://img-blog.csdnimg.cn/6edef1fb1e5b4606870a24120237e35c.png)
输入yml文件内容（可先什么也不写，后面会给出具体代码），选择**Start commit**
![在这里插入图片描述](https://img-blog.csdnimg.cn/93e4ecd7388c43709da2dcff25fa1cf2.png)
新建mian.py（可以在本地调试）和requirements.txt文件，可把python所需库版本放入（可先什么也不写，后面会给出具体代码）

之后点击**Settings**中的**Secrets**添加
![在这里插入图片描述](https://img-blog.csdnimg.cn/a3eb31fc3bbc4f2991586b0d4ec281ba.png)
添加完成后（之前已经给出）：注意城市为北京，秦皇岛......；纪念日和生日格式需与main.py中一致。
![在这里插入图片描述](https://img-blog.csdnimg.cn/a3abac987ae0443eba850793d848d63f.png)
最后，点击**Acrions**里的**morning**，选择**Run workflow**，如果运行成功，则显示绿色对钩，并且用户会收到推送的消息。如运行失败，可以点击查看运行失败的错误信息是什么。
![在这里插入图片描述](https://img-blog.csdnimg.cn/c49e3ef76bfc4deaaad6e31ca8f9b627.png)
代码地址：[https://github.com/QInzhengk/the_milky_way](https://github.com/QInzhengk/the_milky_way)
![在这里插入图片描述](https://img-blog.csdnimg.cn/00896e2580f0428895de352565d84281.png)


## ☕  鸣谢

感谢以下参考的帮助：

- [https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html](https://www.ruanyifeng.com/blog/2019/09/getting-started-with-github-actions.html)
- [https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions](https://docs.github.com/cn/actions/using-workflows/workflow-syntax-for-github-actions)
- [https://github.com/13812851221/-rxrw-daily_morning](https://github.com/13812851221/-rxrw-daily_morning)
- [https://blog.csdn.net/qq_45832050/article/details/126789897](https://blog.csdn.net/qq_45832050/article/details/126789897)
- [https://blog.csdn.net/qq_45832050/article/details/122755904](https://blog.csdn.net/qq_45832050/article/details/122755904)
- [后续更新完将会完善这一部分，有问题可以点击Issues提问；均为互联网资料，侵权删]()
