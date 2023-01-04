function main(splash, args)
  
  
  local num_scrolls = 10
  local scroll_delay = 1
  local scroll_to = splash:jsfunc("window.scrollTo")
  local get_body_height = splash:jsfunc(
  			"function(){return document.body.scrollHeight;}"
  )
  splash.private_mode_enabled = false
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  
  for _ = 1, num_scrolls do
    scroll_to(0,get_body_height())
    assert(splash:wait(scroll_delay))
  end
  
  return {
    html = splash:html(),
    png = splash:png()
  }
end