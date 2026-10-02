import json,sys
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlsplit
requests=[]
release=None
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):self.handle_api('GET')
 def do_POST(self):self.handle_api('POST')
 def do_PATCH(self):self.handle_api('PATCH')
 def handle_api(self,method):
  global release
  path=urlsplit(self.path).path
  body=json.loads(self.rfile.read(int(self.headers.get('Content-Length','0'))) or '{}')
  if path!='/health':
   requests.append({'method':method,'path':path,'body':body})
   with open(sys.argv[1],'w') as f:json.dump(requests,f)
  status=200;data={}
  if path=='/health':data={'ok':True}
  elif path=='/repos/test/node24-smoke/releases/generate-notes':data={'name':'Generated','body':'Generated smoke release notes'}
  elif path=='/repos/test/node24-smoke/releases' and method=='POST':
   release={'id':123,'tag_name':body['tag_name'],'name':body.get('name'),'body':body.get('body'),'draft':body.get('draft',False),'prerelease':False,'assets':[],'created_at':'2026-10-02T00:00:00Z','html_url':'http://127.0.0.1:8765/release/123','upload_url':'http://127.0.0.1:8765/assets{?name,label}',**body};data=release;status=201
  elif path=='/repos/test/node24-smoke/releases' and method=='GET':data=[release] if release else []
  elif path.startswith('/repos/test/node24-smoke/releases/tags/'):
   if release and not release['draft']:data=release
   else:status=404;data={'message':'Not Found'}
  elif path=='/repos/test/node24-smoke/releases/123' and method=='PATCH':release.update(body);data=release
  else:status=404;data={'message':'Unexpected mock endpoint: '+method+' '+path}
  encoded=json.dumps(data).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(encoded)));self.end_headers();self.wfile.write(encoded)
HTTPServer(('127.0.0.1',8765),Handler).serve_forever()
