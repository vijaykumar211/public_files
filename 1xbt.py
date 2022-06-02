from websocket import create_connection
import json,requests
from time import sleep

loip = "aaaaaaa"

ws = create_connection("wss://larmob.com/cafeed")

ws.send('{"protocol":"json","version":1}')
result =  ws.recv()
print("Received '%s'" % result)

ws.send('{"arguments":["00000000-0000-0000-0000-000000000000",434371727,99,"en",7],"invocationId":"0","target":"RegInHub","type":1}')
result =  ws.recv()
print("Received '%s'" % result)


while 5<10:
	sleep(0.1)
	try:
		result =  ws.recv()
		result = result.strip()
		result = bytes(result, 'utf-8').decode('utf-8', 'ignore')
		result = '['+result.replace(" ","").replace('}{','},{').replace(' ]',']')+']'
		results_json = json.loads(result)
		for result_json in results_json:
			#print(result_json)
			target = result_json['target']
			if target=="OnStageChange":
				si = str(result_json['arguments'][0]['si'])
				tb = str(result_json['arguments'][0]['tb'])
				tw = str(result_json['arguments'][0]['tw'])
				print('SI : '+str(si)+', TB : '+str(tb)+', TW : '+str(tw))
				requests.get("http://"+larmob+"/1xbet/conn.php?bd&si="+si+"&tb="+tb+"&tw="+tw)
			if target=="OnCoeffChange":
				print('[+] SI : '+str(si)+', CF : '+str(result_json['arguments'][0]['cf']))
				cf = str(result_json['arguments'][0]['cf'])
				requests.get("http://"+larmob+"/1xbet/conn.php?wd&si="+si+"&cf="+cf)
	except:
 		error = 34873


ws.close()
