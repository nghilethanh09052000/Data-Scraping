function main(splash, args)
  
    splash.private_mode_enabled = false
    assert(splash:go(args.url))
    assert(splash:wait(0.5))
    
    next_page = assert(splash:select("nav > ul > li > a"))
    next_page:mouse_click()
    
    assert(splash:wait(1))
    
    return {
      html = splash:html(),
      png = splash:png()
    }
  end