# -*- coding: utf-8 -*-
from LineAlpha import LineClient
from LineAlpha.LineApi import LineTracer
from LineAlpha.LineThrift.ttypes import Message
from LineAlpha.LineThrift.TalkService import Client
import time, datetime, random ,sys, re, string, os, json, certifi, urllib3, threading

reload(sys)
sys.setdefaultencoding('utf-8')

client = LineClient()
client._qrLogin("line://au/q/")

profile, setting, tracer = client.getProfile(), client.getSettings(), LineTracer(client)
offbot, messageReq, wordsArray, waitingAnswer = [], {}, {}, {}

print client._loginresult()

admin=["uec356cf2190988f335c0b7a020b294e9", "u7af4d5ca6e2681a9845202bc83603043", "u25107bac4622cf71a7797e3d994c2ebb", "u0b17e1c0cf954b314fbfc5a14d10f926"]
wait = {
    'contact':False,
    "lang":"JP",
    "deffGroup":False,
    'readPoint':{},
    'readMember':{},
    'setTime':{},
    'ROM':{}
   }

setTime = {}
setTime = wait["setTime"]

def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text

    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1
    client._client.sendMessage(messageReq[to], mes)

def NOTIFIED_ADD_CONTACT(op):
    try:
        sendMessage(op.param1, client.getContact(op.param1).displayName + " Beni Eklediğin İçin Teşekkürler")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ADD_CONTACT\n\n")
        return

tracer.addOpInterrupt(5,NOTIFIED_ADD_CONTACT)

def autolike():
     for zx in range(0,20):
         hasil = activity(limit=20)
         if hasil['result']['posts'][zx]['postInfo']['liked'] == False:
           try:    
             client.like(hasil['result']['posts'][zx]['userInfo']['mid'],hasil['result']['posts'][zx]['postInfo']['postId'],likeType=1002)
             client.comment(hasil['result']['posts'][zx]['userInfo']['mid'],hasil['result']['posts'][zx]['postInfo']['postId'],"Auto Like by Osmancitci\n\n>>http://line.me/ti/p/~osmancitci")
             print "Like"
           except:
             pass
         else:
             print "Zaten Beğenildi"
     time.sleep(0.01)
     thread2 = threading.Thread(target=autolike)
     thread2.daemon = True
     thread2.start()
        
def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        group_id=op.param1
        #sendMessage(group_id, "Davet \nDon't forget to add our creator bot\ncreated by Fbot" + datetime.datetime.today().strftime('\n\n%H:%M:%S'))
        #sendMessage(group_id, text=None, contentMetadata={'mid': "uec356cf2190988f335c0b7a020b294e9"}, contentType=13)
        print "Grup Davet Kabul : "+group_id
    except Exception as e:
           print e
           print ("\n\nNOTIFIED_INVITE_INTO_GROUP\n\n")
           return

tracer.addOpInterrupt(17, NOTIFIED_INVITE_INTO_GROUP)

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    #print op
    try:
        client.acceptGroupInvitation(op.param1)
        if op.param3 in admin:
            try:
                client.kickoutFromGroup(op.param1,[op.param2])
                client.inviteIntoGroup(op.param1,admin)
            except:
              pass
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_ACCEPT_GROUP_INVITATION\n\n")
        return

tracer.addOpInterrupt(13, NOTIFIED_ACCEPT_GROUP_INVITATION)

def NOTIFIED_KICKOUT_FROM_GROUP(op):
    try:
        if op.param3 in admin:
            try:
                client.kickoutFromGroup(op.param1,[op.param2])
                client.inviteIntoGroup(op.param1,admin)
            except:
              pass
        else:
            sendMessage(msg.to,"Hata ⛔")
        sendMessage(op.param1, client.getContact(op.param3).displayName + " Koruma Devrede\n Sayın Yetkili")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_KICKOUT_FROM_GROUP\n\n")
        return

tracer.addOpInterrupt(19,NOTIFIED_KICKOUT_FROM_GROUP)

def NOTIFIED_LEAVE_GROUP(op):
    try:
        sendMessage(op.param1, client.getContact(op.param2).displayName + " Güle Güle\n Umarım Yeniden Gelirsin..")
    except Exception as e:
        print e
        print ("\n\nNOTIFIED_LEAVE_GROUP\n\n")
        return

tracer.addOpInterrupt(15,NOTIFIED_LEAVE_GROUP)

def NOTIFIED_READ_MESSAGE(op):
    #print op
    try:
        if op.param1 in wait['readPoint']:
            Name = client.getContact(op.param2).displayName
            if Name in wait['readMember'][op.param1]:
                pass
            else:
                wait['readMember'][op.param1] += "\n・" + Name
                wait['ROM'][op.param1][op.param2] = "・" + Name
        else:
            pass
    except:
        pass

tracer.addOpInterrupt(55, NOTIFIED_READ_MESSAGE)

def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
        if msg.contentType == 0:
            try:
                if msg.to in wait['readPoint']:
                    if msg.from_ in wait["ROM"][msg.to]:
                        del wait["ROM"][msg.to][msg.from_]
                else:
                    pass
            except:
                pass
        else:
            pass
    except KeyboardInterrupt:
	       sys.exit(0)
    except Exception as error:
        print error
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)
     
def RECEIVE_MESSAGE(op):
    msg = op.message
    try:
	##test alanı
	if msg.toType == 0:
            if msg.contentType == 0:
                if msg.text == "Mid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "Me":
                    sendMessage(msg.to, text=None, contentMetadata={'mid': msg.from_}, contentType=13)
                
                else:
                    pass
            else:
                pass
				#test alan sn
	
        if msg.toType == 2:
            if msg.contentType == 0:
                if msg.text == "Mid":
                    sendMessage(msg.to, msg.from_)
                if msg.text == "Gid":
                    sendMessage(msg.to, msg.to)
                if msg.text == "Gc":
                    group = client.getGroup(msg.to)
                    ginfo = client.getGroup(msg.to)
                    try:
                        gCreator = ginfo.creator.displayName
                    except:
                        gCreator = "Error"
                        if ginfo.preventJoinByTicket == True:
                            u = "close"
                        else:
                            u = "open"
                    sendMessage(msg.to, text="| Coder |\n" + "Redline Bot\n" + "id line.me/ti/p/~osmancitci\n" + datetime.datetime.today().strftime('\n%H:%M:%S'), contentMetadata={'mid': gCreator}, contentType=13)

                if msg.text == "Ginfo":
                    group = client.getGroup(msg.to)
                    ginfo = client.getGroup(msg.to)
                    try:
                        gCreator = ginfo.creator.displayName
                    except:
                        gCreator = "Error"
                        if ginfo.preventJoinByTicket == True:
                            u = "close"
                        else:
                            u = "open"
                    md = "🏆🔥🎴☬રεɖιίɴε☬🎴🔥🏆 v2.0\n\n[Grup İsmi]\n" + group.name + "\n\n[Grup Id]\n" + group.id + "\n\n[Grup Oluşturan]\n" + gCreator + "\n\n[Grup Resmi]\nhttp://dl.profile.line-cdn.net/" + group.pictureStatus
                    if group.preventJoinByTicket is False: md += "\n\nURL: AÇIK\n"
                    else: md += "\n\nURL: KAPALI\n"
                    if group.invitee is None: md += "\nÜyeler: " + str(len(group.members)) + "\n\nDavetli: 0 Kişi"
                    else: md += "\nÜyeler: " + str(len(group.members)) + " Kişi\nDavetli: " + str(len(group.invitee)) + " Kişi"
                    sendMessage(msg.to,md)
                if "Gn " in msg.text:
                    if msg.from_ in admin:
                        key = msg.text[22:]
                        group = client.getGroup(msg.to)
                        group.name = msg.text.replace("Gn ","")
                        client.updateGroup(group)
                        sendMessage(msg.to,"Grup Adı "+key+" Başarılı Şekilde Değiştirildi.")
                    else:
                        sendMessage(msg.to,"Admin Değilsin... ⛔")
                if msg.text in ["By Redline"]:
                    ginfo = client.getGroup(msg.to)
                    try:
                        client.leaveGroup(msg.to)
                    except:
                          pass
                if "join" in msg.text:
                    if msg.from_ in admin:
                        G = client.getGroup(msg.to)
                        ginfo = client.getGroup(msg.to)
                        G.preventJoinByTicket = False
                        client.updateGroup(G)
                        invsend = 0
                        Ticket = client.reissueGroupTicket(msg.to)
                        client.acceptGroupInvitationByTicket(msg.to,Ticket)
                if "Bc " in msg.text:
		    bctxt = msg.text.replace("Bc ","")
		    sendMessage(msg.to,(bctxt))
	
			
		if msg.text == "Tagall":
                    group = client.getGroup(msg.to)
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    sendMessage(msg.to,"Tagall"+key1)
                    mem = [contact.mid for contact in group.members]
                    for mm in mem:
                        xname = client.getContact(mm).displayName
                        xlen = str(len(xname)+1)
                        msg.contentType = 0
                        msg.text = "@"+xname+" "+key1
                        sendMessage(msg.to, text=None, contentMetadata ={'MENTION':'{"MENTIONEES":[{"S":"0","E":'+json.dumps(xlen)+',"M":'+json.dumps(mm)+'}]}','EMTVER':'4'}, contentType=None)

                    try:
                        client.sendMessage(msg)
                    except Exception as error:
                        print error
                if msg.text == "Url":
                    sendMessage(msg.to,"line://ti/g/" + client._client.reissueGroupTicket(msg.to))
                if msg.text == "Open":
                    if msg.from_ in admin:
                        group = client.getGroup(msg.to)
                        if group.preventJoinByTicket == False:
                            sendMessage(msg.to, "Grup Açık")
                        else:
                            group.preventJoinByTicket = False
                            client.updateGroup(group)
                            sendMessage(msg.to, "URL Açık")
                    else:
                        sendMessage(msg.to,"Admin Değilsin... ⛔")
                if msg.text == "Close":
                    group = client.getGroup(msg.to)
                    if group.preventJoinByTicket == True:
                        sendMessage(msg.to, "Grup Kapalı")
                    else:
                        group.preventJoinByTicket = True
                        client.updateGroup(group)
                        sendMessage(msg.to, "URL Kapalı")
                if "Kick " in msg.text:
                    key = msg.text[5:]
                    client.kickoutFromGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+" Senden Nefret Ediyorum...")
                if "Kill " in msg.text:
                    midd = msg.text.replace("Kill ","")
                    group = client.getGroup(msg.to)
                    client.kickoutFromGroup(msg.to,[midd])
                    sendMessage(msg.to,"🏆🔥🎴☬રεɖιίɴε☬🎴🔥🀀 Grubun'da Terbiyesizlik Yapılamaz... �􏿿􀜁􀅔􏿿􀨁􀄆􀄆􏿿􀜁􀅔􏿿􀨁􀄆")
                if "Nk:" in msg.text:
                    if msg.from_ in admin:
                        _name = msg.text.replace("Nk:","")
                        gs = client.getGroup(msg.to)
                        targets = []
                        for g in gs.members:
                            if _name in g.displayName:
                                targets.append(g.mid)
                        if targets == []:
                            _name = msg.text.replace("Nk:","")
                            gs = client.getGroup(msg.to)
                            targets.append(g.name)
                            sendMessage(msg.to," Tamamdır.")
                        else:
                            for target in targets:
                                try:
                                    client.kickoutFromGroup(msg.to,[target])
                                except:
                                    sendText(msg.to,"Hata ⛔")
                    else:
                        sendMessage(msg.to,"Admin Değilsin... ⛔")     
                if msg.text == "Cancel":
                    group = client.getGroup(msg.to)
                    if group.invitee is None:
                        sendMessage(op.message.to, "Aktif Davet İptali Yok...")
                    else:
                        gInviMids = [contact.mid for contact in group.invitee]
                        client.cancelGroupInvitation(msg.to, gInviMids)
                        sendMessage(msg.to, str(len(group.invitee)) + " Adet Davet İptal Edildi")
                if "Invite:" in msg.text:
                    key = msg.text[-33:]
                    client.findAndAddContactsByMid(key)
                    client.inviteIntoGroup(msg.to, [key])
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+" Seni Davet Ettim.")
                if msg.text == "Me":
                    M = Message()
                    M.to = msg.to
                    M.contentType = 13
                    M.contentMetadata = {'mid': msg.from_}
                    client.sendMessage(M)
                if "Show:" in msg.text:
                    key = msg.text[-33:]
                    sendMessage(msg.to, text=None, contentMetadata={'mid': key}, contentType=13)
                    contact = client.getContact(key)
                    sendMessage(msg.to, ""+contact.displayName+"' Kullanıcısın Hesabı..")
                if msg.text == "Time":
                    sendMessage(msg.to, "Şu Anki Zaman\n" + datetime.datetime.today().strftime('%Y<~Yıl %m<~Ay %d<~Gün %H:%M:%S') + "\n")
                if msg.text == "Clock":
                    sendMessage(msg.to, "Şu Anki Saat\n" + datetime.datetime.today().strftime('%H:%M:%S'))
                if msg.text == "Gift":
                        sendMessage(msg.to, text="Hediyemi Göndermek İstiyorsun?\nHediye Listesi:\n~>Gift 1\n~>Gift 2\n~>Gift 3\n~>Gift 4\n~>Gift 5\n~>Gift 6\n~>Gift 7", contentMetadata=None, contentType=None)
                if msg.text == "Gift 2":
                        sendMessage(msg.to, text="gift sent", contentMetadata={'PRDID': 'a0768339-c2d3-4189-9653-2909e9bb6f58',
                                    'PRDTYPE': 'THEME',
                                    'MSGTPL': '5'}, contentType=9)
                if msg.text == "Gift 1":
                        sendMessage(msg.to, text="gift sent", contentMetadata={'PRDID': '2df50b22-112d-4f21-b856-f88df2193f9e',
                                    'PRDTYPE': 'THEME',
                                    'MSGTPL': '8'}, contentType=9)
                if msg.text == "Gift 3":
                        sendMessage(msg.to, text="gift sent", contentMetadata={'PRDID': 'dc1e9626-7594-4561-a86e-5891910c96f3',
                                    'PRDTYPE': 'THEME',
                                    'MSGTPL': '7'}, contentType=9) 
                if msg.text == "Gift 4":
                        sendMessage(msg.to, text="gift sent", contentMetadata={'PRDID': '40ed630f-22d2-4ddd-8999-d64cef5e6c7d',
                                    'PRDTYPE': 'THEME',
                                    'MSGTPL': '6'}, contentType=9)
                if msg.text == "Gift 5":
                        sendMessage(msg.to, text="gift sent", contentMetadata={'STKPKGID': '9490',
                                    'PRDTYPE': 'STICKER',
                                    'MSGTPL': '2'}, contentType=9)
                if msg.text == "Gift 6":
                        sendMessage(msg.to, text="gift sent", contentMetadata={'STKPKGID': '9578',
                                    'PRDTYPE': 'STICKER',
                                    'MSGTPL': '3'}, contentType=9)
                if msg.text == "Gift 7":
                        sendMessage(msg.to, text="gift sent", contentMetadata={'STKPKGID': '9504',
                                    'PRDTYPE': 'STICKER',
                                    'MSGTPL': '4'}, contentType=9)
                if msg.text == "Author":
                    sendMessage(msg.to, text="| Coder |\n" + "Redline Bot\n" + "id line.me/ti/p/~osmancitci\n" + datetime.datetime.today().strftime('\n%H:%M:%S'), contentMetadata={'mid': "uec356cf2190988f335c0b7a020b294e9"}, contentType=13)
                if msg.text in ["Sp","Speed","speed"]:
                    if msg.from_ in admin:
                        start = time.time()
                        sendMessage(msg.to, text="Lütfen Bekleyiniz...", contentMetadata=None, contentType=None)
                        elapsed_time = time.time() - start
                        sendMessage(msg.to, "%s Saniye" % (elapsed_time))
                    else:
                        sendMessage(msg.to,"Admin Değilsin... ⛔")
                if msg.text == "Responsename":
                    if msg.from_ in admin:
                        sendMessage(msg.to,"Sen Kralsın™")
                    else:
                        sendMessage(msg.to,"Admin Değilsin... ⛔")
                if "Cm:" in msg.text:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    sendMessage(msg.to,"Mid : "+key1)
                if "Cp:" in msg.text:
                    key = eval(msg.contentMetadata["MENTION"])
                    key1 = key["MENTIONEES"][0]["M"]
                    contact = client.getContact
					
                    try:
                        cu = client.channel.getCover(msg.contentMetadata["mid"])
                    except:
                           cu = ""
                    md = "[displayName]:\n" + contact.name + "\n[mid]:\n" +key1 + "\n[statusMessage]:\n" + contact.statusMessage + "\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n[coverURL]:\n" + str(cu)
                    sendMessage(msg.to,md)
                if "random:" in msg.text:
                    if msg.from_ in admin:
                        strnum = msg.text.replace("random:","")
                        elapsed_time = time.time() - start
                        try:
                            num = int(strnum)
                            for var in range(0,num):
                                name = "".join([random.choice + "%s Saniye" %(elapsed_time) for x in xrange(10)])
                                time.sleep(0.01)
                        except:
                            sendMessage(msg.to,"Hata ⛔")
                    else:
                        sendMessage(msg.to,"Admin Değilsin... ⛔")
                if "Random:" in msg.text:
                    if msg.from_ in admin:
                        strnum = msg.text.replace("Random:","")
                        source_str = 'abcdefghijklmnopqrstuvwxyz1234567890@:;./_][!&%$#)(=~^|'
                        try:
                            num = int(strnum)
                            group = client.getGroup(msg.to)
                            for var in range(0,num):
                                name = "".join([random.choice(source_str) for x in xrange(10)])
                                time.sleep(4)
                                group.name = name
                                client.updateGroup(group)
                        except:
                            sendMessage(msg.to,"Hata ⛔")
                    else:
                        sendMessage(msg.to,"Admin Değilsin... ⛔")
                if msg.text in ["555","555+"]:
                    sendMessage(msg.to, text=None, contentMetadata={"STKID": "100",
                                     "STKPKGID": "1",
                                     "STKVER": "100"}, contentType=7)
									
                    #if "Gn " in msg.text:
                if msg.text in ["Owner","owner","Admin","admin","Yetkili","yetkili"]:
					if msg.from_ in admin:
						sendMessage(msg.to,"🏆🔥🎴☬રεɖιίɴε☬🎴🔥🏆 v2.0\n\n" +
                                       "⭐🏆🔥| Coder |🔥🏆⭐\n\n" +
                                       "🏆 Mid [MID Numaran]\n" +
                                       "🏆 Gid [Grup ID]\n" +
                                       "🏆 Nk: [Tüm Üyeleri Siler]\n" +
                                       "🏆 Gn [Grup Adı Değiştirir]\n" +
                                       "🏆 Ginfo [Grup Bilgisi]\n" +
                                       "🏆 Cancel [Bekleyen Davetleri Siler]\n" +
                                       "🏆 Sp,Speed,speed [Bot Hızı]\n" +
                                       "🏆 Time [Saat Gösterir]\n" +  
                                       "🏆 Me [Senin Kontakt Linkin]\n" +
                                       "🏆 Show: [Sadece MID]\n" +
                                       "🏆 Url [URL Grup]\n" +
                                       "🏆 Open [URL Alımını Açar]\n" +
                                       "🏆 Close [Url Alımını Durdurur]\n" +
                                       "🏆 Kick [Sadece MID]\n" + 
                                       "🏆 Invite: [Sadece MID]\n" +
                                       "🏆 Gift [Hediye Yolla]\n" +
                                       "🏆 Author [Coder]\n" +
                                       "🏆 Responsename\n" +
                                       "🏆 Cm:[@tagmodu][MID Gösterir]\n" +
                                       "🏆 Random: [Grup İsmi Değiştirir.]\n" +
                                       "🏆 Bc [Yazı Yazdırır]\n" +
                                       "🏆 Clock [Saat Gösterir]\n" +
									   "🏆 Check [Okuma Ayarlar]\n" +
									   "🏆 Siders [Okuyanları Gösterir]\n" +
                                       "🏆 random: [Grup Adı Değiştirir(hız)]\n\n" +
                                       "🏆🔥🎴☬રεɖιίɴε☬🎴🔥🏆\n" + datetime.datetime.today().strftime('\n%H:%M:%S'), contentMetadata=None, contentType=None)
					else:
						sendMessage(msg.to,"Admin Değilsin... ⛔")
                if msg.text in ["Yardım","yardım"]:
                    sendMessage(msg.to,"🏆🔥🎴☬રεɖιίɴε☬🎴🔥🏆 v2.0\n\n" +
                                       "⭐🏆🔥| Coder's |🔥🏆⭐\n\n" +
                                       "☬ Mid [MID Numaran]\n" +
                                       #"☬ Gid [Grup ID]\n" +
                                       #"☬ Nk: [Sadece Admin]\n" +
                                       #"☬ Gn [Sadece Admin]\n" +
                                       "☬ Ginfo [Grup Bilgisi]\n" +
                                       #"☬ Cancel [Bekleyen Davetleri Siler]\n" +
                                       #"☬ Sp,Speed,speed [Bot Hızı]\n" +
                                       "☬ Time [Saat Gösterir]\n" +  
                                       "☬ Me [Senin Kontakt Linkin]\n" +
                                       #"☬ Show: [Sadece MID]\n" +
                                       #"☬ Url [URL Grup]\n" +
                                       #"☬ Open [Sadece Admin]\n" +
                                       #"☬ Close [Url Alımını Durdurur]\n" +
                                       #"☬ Kick [ID ye Göre Atma]\n" + 
                                       #"☬ Invite: [ID ye Göre Davet]\n" +
                                       "☬ Gift [Hediye Yolla]\n" +
                                       "☬ Author [Coder]\n" +
                                       "☬ Responsename [Sahip]\n" +
                                       "☬ Clock [Saat Gösterir]\n" +
                                       #"☬ Cm:[@tagmodu][MID Gösterir]\n" +
                                       #"☬ Random: [Sadece Admin]\n" +
                                       "☬ Bc [Yazı Yazdırır]\n\n" +
                                       "🏆🔥🎴☬રεɖιίɴε☬🎴🔥🏆\n" + datetime.datetime.today().strftime('\n\n%H:%M:%S'), contentMetadata=None, contentType=None)
                if msg.text == "Check":
                    sendMessage(msg.to, "Okuma Noktası Ayarlandı... \n「Siders」 Komutu İle Görebilirsiniz." + datetime.datetime.today().strftime('\n\n%H:%M:%S'))
                    try:
                        del wait['readPoint'][msg.to]
                        del wait['readMember'][msg.to]
                    except:
                        pass
                    wait['readPoint'][msg.to] = msg.id
                    wait['readMember'][msg.to] = ""
                    wait['setTime'][msg.to] = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    wait['ROM'][msg.to] = {}
                    print wait
                if msg.text == "Siders":
                    if msg.to in wait['readPoint']:
                        if wait["ROM"][msg.to].items() == []:
                            chiya = ""
                        else:
                            chiya = ""
                            for rom in wait["ROM"][msg.to].items():
                                print rom
                                chiya += rom[1] + "\n"

                        sendMessage(msg.to, "Okuyan Üyeler %s\n\nOkumayı Engelleyen Üyeler\n%s🏆🔥🎴☬રεɖιίɴε☬🎴🔥🏆\n\nOluşturulma Tarihi\n[%s]"  % (wait['readMember'][msg.to],chiya,setTime[msg.to]))
                    else:
                        sendMessage(msg.to, "Henüz Ayarlanmadı\n「Check」 Komutunu Kullanarak Listeyi Yenileyiniz.")
                else:
                    pass
        else:
            pass

    except Exception as e:
        print e
        print ("\n\nRECEIVE_MESSAGE\n\n")
        return

tracer.addOpInterrupt(26, RECEIVE_MESSAGE)

while True:
    tracer.execute()
