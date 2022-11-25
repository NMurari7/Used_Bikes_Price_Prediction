import streamlit as st
import numpy as np
import pickle
import re
from datetime import date

# from sklearn.ensemble import RandomForestRegressor

# import the model
pipe = pickle.load(open('model.pkl','rb'))
df = pickle.load(open('df.pkl','rb'))

st.title("Used Bike Price Predictor")

# brand
brands_dic = {'Bajaj': 10806, 'Hero': 6068, 'Royal Enfield': 3926, 'Yamaha': 3720, 'Honda': 1926, 'Suzuki': 1340, 'TVS': 1092, 'KTM': 999, 'Harley-Davidson': 714, 'Hyosung': 46, 'Mahindra': 35, 'Benelli': 31, 'Kawasaki': 26}
brands_list = [brand for brand in brands_dic.keys()]
pre_brand = st.selectbox('Brand',brands_list)
brand = brands_dic.get(pre_brand)

# Bike name
bikes_dic = {'Bajaj Pulsar 150cc': 2776, 'Bajaj Avenger Street 220': 2531, 'Bajaj Avenger 220cc': 2060,
 'Royal Enfield Classic 350cc': 1673, 'Hero Passion Pro 100cc': 1432, 'Hero Passion 100cc': 1238,
 'Royal Enfield Thunderbird 350cc': 919, 'Yamaha YZF-R15 2.0 150cc': 769, 'Royal Enfield Bullet Electra 350cc': 756,
 'Bajaj Pulsar NS200': 708, 'KTM RC 390cc': 705, 'Bajaj Dominar 400 ABS': 700, 'Hero CD Deluxe 100cc': 693,
 'Bajaj Platina 100cc': 686, 'Hero CBZ Xtreme 150cc': 686, 'Honda CB Trigger 150cc': 681, 'TVS Apache RTR 180cc': 675,
 'Yamaha Fazer 150cc': 674, 'Yamaha FZ 150cc': 661, 'Hero Super Splendor 125cc': 649, 'Honda CB Hornet 160R STD': 641,
 'Harley-Davidson Street 750 ABS': 631, 'Hero Hunk Rear Disc 150cc': 619, 'Suzuki Slingshot Plus 125cc': 617,
 'Yamaha SZ-RR 150cc': 613, 'Yamaha Fazer 25 250cc': 613, 'Suzuki Zeus 125cc': 608, 'Hero Splendor Plus 100cc': 189,
 'Honda CB Shine 125cc': 171, 'Bajaj V15 150cc': 159, 'Bajaj Avenger Street 150': 150, 'TVS Apache RTR 160cc': 134,
 'Yamaha FZs 150cc': 127, 'KTM Duke 390cc': 124, 'Bajaj Pulsar RS200 ABS': 123, 'KTM RC 200cc': 111,
 'Bajaj Discover 125cc': 105, 'Royal Enfield Thunderbird 500cc': 103, 'Hero HF Deluxe 100cc': 101, 'Bajaj Pulsar 220cc': 98,
 'Bajaj Pulsar 180cc': 93, 'KTM Duke 200cc': 90, 'Royal Enfield Classic 500cc': 89, 'Bajaj Pulsar RS200': 80,
 'Bajaj CT 100 100cc': 80, 'Hero Passion Plus 100cc': 79, 'Bajaj Discover 100cc': 79, 'Bajaj Pulsar 135LS': 78,
 'Honda CBF Stunner 125cc': 76, 'Bajaj Avenger Cruise 220': 72, 'Honda CBR 150R 150cc': 71, 'Honda CB Unicorn 150cc': 71,
 'Yamaha YZF-R15 150cc': 69, 'Bajaj Pulsar 220F': 68, 'Harley-Davidson Street 750': 66, 'Hero Splendor Pro 100cc': 62,
 'Suzuki Gixxer 150cc': 62, 'Royal Enfield Bullet Twinspark 350cc': 58, 'Royal Enfield Bullet 350cc': 57,
 'Honda Dream Yuga 110cc': 56, 'Hero Karizma R 223cc': 56, 'TVS Sport 100cc': 54, 'Royal Enfield Classic Desert Storm 500cc': 54,
 'Yamaha FZ16 150cc': 51, 'Hero Passion Xpro 110cc': 51, 'Royal Enfield Himalayan 410cc': 51, 'Royal Enfield Bullet Electra Twinspark 350cc': 50,
 'Bajaj Discover 135cc': 46, 'Yamaha FZ S V 2.0 150cc': 45, 'Hero Splendor iSmart 110cc': 43, 'Honda CBR 250R': 42,
 'Yamaha YZF-R15 V3 150cc': 41, 'TVS Apache RTR 200 4V Carburetor': 40, 'Yamaha FZ25 250cc': 40, 'Honda CB Twister 110cc': 40,
 'Hero Hunk 150cc': 38, 'Bajaj Pulsar AS150': 38, 'TVS Star City Plus 110cc': 37, 'Hero Karizma ZMR 223cc': 37,
 'Hero Glamour 125cc': 37,
 'Suzuki Gixxer SF 150cc': 36,
 'Bajaj Discover 125ST': 35,
 'Yamaha SZR 150cc': 35,
 'TVS Star City 110cc': 35,
 'Bajaj Platina  Alloy ES-100cc': 34,
 'Honda CB Hornet 160R CBS': 33,
 'Royal Enfield Standard 350cc': 33,
 'Hero Splendor 100cc': 32,
 'Bajaj Pulsar 200 NS 200cc': 31,
 'TVS Apache RR310': 31,
 'Bajaj Discover 100M': 31,
 'Bajaj Pulsar AS200': 30,
 'Royal Enfield Electra 350cc': 30,
 'Royal Enfield Classic Chrome 500cc': 30,
 'Hero Ignitor 125cc': 30,
 'Honda Livo 110cc': 29,
 'Suzuki Intruder 150cc': 29,
 'Bajaj Dominar 400': 27,
 'Royal Enfield\u200e Bullet 350cc': 27,
 'Harley-Davidson Iron 883': 27,
 'KTM Duke 250cc': 27,
 'Hyosung GT250R': 25,
 'Bajaj  Pulsar 180cc': 25,
 'Mahindra Centuro 110cc': 25,
 'Hero Splendor iSmart 100cc': 24,
 'Yamaha FZ V 2.0 150cc': 24,
 'Royal Enfield Classic Gunmetal Grey 350cc': 24,
 'Bajaj Discover 150cc': 24,
 'Hero Passion Pro i3S Alloy 100cc': 24,
 'TVS Star Sport 100cc': 23,
 'Royal Enfield Continental GT 535cc': 23,
 'Honda CBR 250R ABS': 23,
 'Kawasaki Ninja 650cc': 22,
 'Bajaj Pulsar NS160': 22,
 'TVS Apache RTR 180cc ABS': 22,
 'Benelli TNT 300': 22,
 'Royal Enfield Standard 500cc': 20,
 'Yamaha YZF-R15 S 150cc': 20,
 'TVS Apache RTR 160 4V Disc': 20,
 'TVS Apache RTR 200 4V Fi': 18,
 'Bajaj Discover 125M': 17,
 'Mahindra Mojo 300cc': 16,
 'Bajaj V12 125cc': 15,
 'Bajaj Discover 110cc': 15,
 'Bajaj Discover 150F': 15,
 'Hero Splendor Plus Self Alloy 100cc': 14,
 'Honda CB Unicorn 160': 14,
 'Honda CD 110 Dream': 14,
 'Hyosung GT650R': 14,
 'Royal Enfield Classic Stealth Black 500cc': 14,
 'Royal Enfield Bullet 500cc': 14,
 'TVS Apache RTR 200 4V FI': 14,
 'TVS Apache RTR 200 4V ABS': 14,
 'TVS Apache 150cc': 13,
 'Honda Livo Disc 110cc': 13,
 'TVS Apache RTR 200 4V ABS Race Edition': 13,
 'Honda CB Unicorn 160 STD': 13,
 'Hero CBZ 150cc': 13,
 'Hero Honda Splendor 100cc': 13,
 'Royal Enfield Thunderbird X 350cc': 13,
 'Benelli TNT 25 250cc': 13,
 'Hyosung Aquila GV250': 12,
 'Royal Enfield Thunderbird X 350cc ABS': 12,
 'Hero HF Deluxe Eco 100cc': 12,
 'Kawasaki Ninja 300cc': 12,
 'Yamaha FZS FI 150cc': 12,
 'Royal Enfield Bullet Twinspark 500cc': 11,
 'Royal Enfield Himalayan 410cc Fi ABS': 11,
 'Honda CB Unicorn 160 CBS': 11,
 'Hero Honda Splendor Plus 100cc': 11,
 'Royal Enfield Interceptor 650cc': 11,
 'Hero Splendor NXG 100cc': 11}  # bajaj:24
bikes_list = [bike for bike in bikes_dic.keys()]
bikes_li = []
for i in bikes_list:
 if str(pre_brand)[:2] == str(i)[:2]:
  # st.title(str(pre_brand) + str(i))
  bikes_li.append(i)

pre_bike_model = st.selectbox("Bike_name", bikes_li)
bike_model = bikes_dic.get(pre_bike_model)

# CC
# cc_list = [150, 100, 220, 350, 125, 200, 160, 180, 390, 250, 400, 750, 110, 500, 135, 223, 650, 410, 300, 310, 883, 535,
#            1000, 1200, 800, 600, 295, 320, 1300, 900, 302, 765, 797, 675, 959, 865, 149, 1130, 502, 899, 850, 1050, 1262,
#            796, 1090, 1198, 175, 1700, 1100, 1800, 1299, 821, 107]
# cc = st.selectbox("CC",df['power'].unique())

cc = re.findall(r'\d+', pre_bike_model)[-1]
# cc = int(pre_bike_model[-6:-2])


# kms driven
km = st.number_input('Kms Driven', min_value=1, max_value=500000, value=10000)

# owner type
owner = st.number_input("Owner Type (eg:- first hand, second hand)",min_value=1,max_value=4)

# city
cities_dic = {'Delhi': 7318,
 'Bangalore': 2723,
 'Mumbai': 2591,
 'Hyderabad': 2160,
 'Pune': 1724,
 'Chennai': 1619,
 'Lucknow': 1294,
 'Jaipur': 1007,
 'Ghaziabad': 938,
 'Ahmedabad': 905,
 'Noida': 776,
 'Bhopal': 651,
 'Gautam Buddha Nagar': 649,
 'Kanchipuram': 640,
 'Jodhpur': 635,
 'Karnal': 625,
 'Rupnagar': 621,
 'Allahabad': 621,
 'Gurgaon': 617,
 'Godhara': 611,
 'Faridabad': 609,
 'Kadapa': 608,
 'Perumbavoor': 608,
 'Ludhiana': 100,
 'Kolkata': 97,
 'Thane': 94,
 'Jhansi': 87,
 'Vadodara': 75,
 'Surat': 57,
 'Jalandhar': 52,
 'Chandigarh': 46,
 'Rajkot': 36,
 'Indore': 33,
 'Dehradun': 30,
 'Patna': 29,
 'Navi Mumbai': 27,
 'Nagpur': 27,
 'Coimbatore': 25,
 'Tiruvallur': 23,
 'Guwahati': 23,
 'Bhubaneshwar': 22,
 'Howrah': 21,
 'Kanpur': 19,
 'Aurangabad': 18,
 'Cuttack': 17,
 'Visakhapatnam': 16,
 'Alibag': 15,
 'Alipore': 14,
 'Kalyan': 13,
 'Nashik': 13,
 'Ranchi': 13,
 'Udaipur': 12,
 'Rohtak': 12,
 'Agra': 12,
 'Kota': 12,
 'Gorakhpur': 12,
 '24 Pargana': 11,
 'Ernakulam': 11,
 'Gandhinagar': 11,
 'Meerut': 11}
cities_list = [city for city in cities_dic.keys()]
city = st.selectbox("city", cities_list)
city = cities_dic.get(city)

# year
from datetime import datetime
present_year = date.today().year
year = st.slider(
    "Year",min_value=1970, max_value=present_year, value=2015)

# year = st.number_input("year",min_value=1970,max_value=present_year)
year = present_year-year


if st.button('Predict Price'):
    query = np.array([bike_model, city, km, owner, year, cc, brand])
    # st.title([bike_model, city, km, owner, year, cc, brand])
    query = query.reshape(1,7)
    price = int(pipe.predict(query))
    if year == 0 and price > 100000:
     st.title("The predict price of " + pre_bike_model + " is " + str(price+35000))
    elif year <=2 and price > 100000:
     st.title( "The predict price of "+ pre_bike_model + " is "+ str(price+30000) )
    elif year > 10 and price > 100000:
     st.title("The predict price of " + pre_bike_model + " is " + str(price-30000))
    else:
     st.title("The predict price of " + pre_bike_model + " is " + str(price))

#
# if __name__ == "__main__" :
#     app.run(host='0.0.0.0', port=8080)