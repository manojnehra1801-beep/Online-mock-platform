from flask import Flask, request, session, redirect
import time

app = Flask(__name__)
app.secret_key = "manojnehra2025"

PER_MARK = 1
NEG_MARK = 0.25
Q_TIME = 30

QUESTIONS = [
("Which of the following is NOT a cropping season in India?\nभारत में फसल का मौसम नहीं है?",
["Kharif","Rabi","Zaid","Barani"],3),

("Kadbanwadi grassland is in –\nकदबनवाड़ी घास का मैदान कहाँ है?",
["Tamil Nadu","Andhra Pradesh","Odisha","Maharashtra"],3),

("Which port faces silt problem in Hugli river?\nहुगली नदी में गाद की समस्या किस पोर्ट को है?",
["Kolkata","Kochchi","Tuticorin","Chennai"],0),

("Decline in mortality (1921-51) was due to –\n1921-51 में मृत्यु दर घटने का कारण?",
["War","Improved health & sanitation","Birth rate","AI"],1),

("Approx % of plateau region in India?\nभारत में पठारी क्षेत्र का प्रतिशत?",
["5%","12%","27%","59%"],2),

("Birth rate > Death rate means population will –\nजन्म दर अधिक होने पर जनसंख्या?",
["Increase","Decrease","Same","None"],0),

("Sudasari GIB breeding centre is in –\nसुदासरी बस्टर्ड केंद्र कहाँ है?",
["Rajasthan","TN","Kerala","Karnataka"],0),

("Origin of universe theory –\nब्रह्मांड की उत्पत्ति का सिद्धांत?",
["Big Bang","Plate","Quantum","String"],0),

("ST population % in India (2025) –\nभारत में ST जनसंख्या प्रतिशत?",
["8.6","5.5","9.8","12.2"],3),

("NOT hinterland of Marmagao port –\nमार्मगाओ पोर्ट का पृष्ठप्रदेश नहीं?",
["Karnataka","Goa","South Maharashtra","Himachal Pradesh"],3),

("Main processes of population change –\nजनसंख्या परिवर्तन की मुख्य प्रक्रियाएँ?",
["3","5","6","7"],0),

("NOT a dryland crop –\nशुष्क फसल नहीं है?",
["Guar","Bajra","Jute","Ragi"],2),

("Navratna CPSE (2025) –\nनवरत्न कंपनी?",
["RCFL","SAIL","REC","HPCL"],0),

("Badampahar mines are famous for –\nबादामपहाड़ खदानें प्रसिद्ध हैं?",
["Iron ore","Dolomite","Limestone","Bauxite"],0),

("Incorrect about Deendayal Port –\nदीनदयाल पोर्ट पर गलत कथन?",
["Kandla name","Major port","Eastern India","Petroleum"],2),

("East–West corridor length –\nपूर्व-पश्चिम कॉरिडोर की लंबाई?",
["2900 km","3640 km","4700 km","5860 km"],2),

("Amrabad Tiger Reserve is in –\nअमराबाद टाइगर रिज़र्व कहाँ है?",
["Kerala","MP","Telangana","TN"],2),

("97% coal lies in valleys –\n97% कोयला किन घाटियों में है?",
["Damodar–Sone–Mahanadi–Godavari","Ganga","Narmada","Indus"],0),

("Dryland crop –\nशुष्क फसल?",
["Rice","Sugarcane","Jute","Ragi"],3),

("State with 100 million+ population –\n100 मिलियन से अधिक जनसंख्या वाला राज्य?",
["WB","MP","Bihar","Rajasthan"],2),

("Kaladan project connects India with –\nकलादान परियोजना किस देश से जुड़ी है?",
["Nepal","Pakistan","Bangladesh","Myanmar"],3),

("Petrapole rail link is between –\nपेट्रापोल रेल लिंक किनके बीच है?",
["India–Bhutan","India–Nepal","India–Bangladesh","India–Myanmar"],2),

("Urbanisation in India (2011) –\nभारत में शहरीकरण 2011 में?",
["31.16%","41.16%","21.16%","45.16%"],0),

("2nd largest rhino habitat –\nदूसरा सबसे बड़ा गैंडा आवास?",
["Kaziranga","Jaldapara","Gir","Kanha"],1),

("Ramgarh Vishdhari Tiger Reserve –\nरामगढ़ विषधारी टाइगर रिज़र्व?",
["Rajasthan","Karnataka","Odisha","Jharkhand"],0),

("Iron ore hill ranges in –\nलौह अयस्क पहाड़ियाँ कहाँ हैं?",
["AP","TN","Odisha","Meghalaya"],2),

("Indira Gandhi Canal originates from –\nइंदिरा गांधी नहर कहाँ से निकलती है?",
["Punjab","Rajasthan","UK","Haryana"],0),

("Umred–Pauni–Karhandla Sanctuary –\nउमरेड-पौनी-करहंडला अभयारण्य?",
["Maharashtra","Gujarat","UK","Punjab"],0),

("107th National Park of India –\nभारत का 107वाँ राष्ट्रीय उद्यान?",
["Simlipal","Bhitarkanika","Satkosia","Nandankanan"],0),

("SECC 2011 conducted by –\nSECC 2011 किसने कराया?",
["Ministry of Rural Dev","Housing Ministry","Both","None"],0),

("First complete census in India –\nभारत की पहली पूर्ण जनगणना?",
["1830","1810","1840","1820"],1),

("Second largest religion in India –\nभारत का दूसरा सबसे बड़ा धर्म?",
["Christian","Sikh","Muslim","Buddhist"],2),

("Hirakud dam is on river –\nहीराकुंड बाँध किस नदी पर है?",
["Periyar","Krishna","Mahanadi","Indus"],2),

("Universe became transparent after –\nब्रह्मांड कब पारदर्शी हुआ?",
["300000 yrs","3000 yrs","30000 yrs","300 yrs"],0),

("Caste census till –\nजाति जनगणना कब तक हुई?",
["1921","1911","1931","1901"],2),

("Literacy in 1951 –\n1951 में साक्षरता?",
["18.33%","28.33%","10.33%","9.33%"],0),

("State rich in marble & sandstone –\nसंगमरमर व बलुआ पत्थर से समृद्ध राज्य?",
["Kerala","AP","Odisha","Rajasthan"],3),

(">85% irrigated state –\n85% से अधिक सिंचित राज्य?",
["Bihar","Odisha","MP","Haryana"],3),

("Migration factors –\nप्रवासन के कारक?",
["2","3","4","5"],0),

("Rural roads % –\nग्रामीण सड़कों का प्रतिशत?",
["80%","60%","40%","20%"],0),

("SECC 2011 districts –\nSECC 2011 में जिले?",
["640","680","750","730"],3),

("SECC households (crore) –\nSECC परिवार (करोड़)?",
["24.49","27.97","11.97","31.28"],1),

("Navigable waterways length –\nनौगम्य जलमार्गों की लंबाई?",
["6500 km","8000 km","11200 km","14500 km"],2),

("Negative population growth state –\nनकारात्मक जनसंख्या वृद्धि वाला राज्य?",
["Nagaland","Mizoram","Daman","Lakshadweep"],0),

("Temperate & subtropical crop –\nसमशीतोष्ण व उपोष्णकटिबंधीय फसल?",
["Wheat","Jute","Cotton","Cucumber"],0),

("Sunlight reaches Earth in –\nसूर्य का प्रकाश पृथ्वी तक पहुँचता है?",
["3 min","5 min","8 min","15 min"],2),

("India’s coastline length –\nभारत की तटरेखा की लंबाई?",
["7516 km","11098.8 km","13065.6 km","15035.5 km"],2)
]

# (Rest of the code remains same as last version)