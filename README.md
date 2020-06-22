# python_blog

**day_01:**

app = web.Application(loop=loop)
loop循环参数取消改为
app = web.Application()

app.make_handler()方法弃用

    # srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    # logging.info('server started at http://127.0.0.1:9000...')
    # return srv
    改写为：
    # runner = web.AppRunner(app)
    # await runner.setup()
    # site = web.TCPSite(runner, 'localhost', 8080)
    # await site.start()

  