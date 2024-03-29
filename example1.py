from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from scipy.stats import norm
from geoalchemy2 import Geometry
from sqlalchemy import func
import numpy as np

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:zxc789@localhost:5432/POIs'

db = SQLAlchemy(app)

class HangzhouPOI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    __tablename__ = 'hangzhou_poi'
    name = db.Column(db.String(100), nullable=False)
    head_class = db.Column(db.String(100), nullable=False)
    small_class = db.Column(db.String(100), nullable=False)
    lon = db.Column(db.Numeric, nullable=False)
    lat = db.Column(db.Numeric, nullable=False)
    geom = db.Column(Geometry('POINT', srid=32651))
    

@app.route('/poi/<int:id>', methods=['GET'])
def get_poi(id):
    poi = HangzhouPOI.query.get(id)
    if poi is None:
        return jsonify({'error': 'POI not found'}), 404

    return jsonify({
        'id': poi.id,
        'name': poi.name,
        'head_class': poi.head_class,
        'small_class': poi.small_class,
        'lon': float(poi.lon),
        'lat': float(poi.lat)
    })

@app.route('/poi/<center_lon>/<center_lat>/<radius>/<head_class>', methods=['GET'])
def get_pois_in_circle(center_lon, center_lat, radius,head_class):
    try:
        circle_center_lon = float(center_lon)
        circle_center_lat = float(center_lat)
        circle_radius = 0.88*float(radius)
        head_class = head_class
    except ValueError:
        return jsonify({'error': 'Invalid parameter type'}), 400

    # 转换圆心坐标为 EPSG:32651 坐标系
    transformed_circle_center = func.ST_Transform(func.ST_SetSRID(func.ST_MakePoint(circle_center_lon, circle_center_lat), 4326), 32651)

    # 创建圆的几何对象
    circle_geom = func.ST_Buffer(transformed_circle_center, circle_radius)

    result = HangzhouPOI.query.filter(func.ST_DWithin(HangzhouPOI.geom, circle_geom, 0)).all()
    # 查询在圆内的点，并根据head_class筛选
    if head_class != 'all':
       selected_result = [poi for poi in result if poi.head_class == head_class]
    else:
        selected_result = result
    
    # 统计不同head_class的数量和对应数据个数
    result_count = db.session.query(HangzhouPOI.head_class, func.count()).filter(HangzhouPOI.id.in_([poi.id for poi in result])).group_by(HangzhouPOI.head_class).all()
    #return result_count
    # 创建一个字典来存储不同head_class和对应的数据个数
    head_class_counts = {row[0]: row[1] for row in result_count}
    #计算pi
    pi=[count/len(result) for count in head_class_counts.values()]
    #计算熵
    entropy=-sum([p*np.log(p) for p in pi])
    #归一化
    diversity_score=entropy/np.log(12)*100

    def gaussian(x,  sigma=1000,mu=0,):
        # x = 2.5  # 输入值
        # mu = 0  # 均值
        # sigma   # 标准差
        cdf_value = norm.cdf(x, mu, sigma)

        return cdf_value
    #计算距离得分
    dis_score_list=[]
    for poi in selected_result:
        distance = distance = db.session.query(func.ST_Distance(func.ST_Transform(poi.geom, 32651), transformed_circle_center)).scalar()
        distance_score = gaussian(distance,circle_radius/4)
        # distance_score=1/(1+distance)
        dis_score_list.append(distance_score)
    dis_score=sum(dis_score_list)
    # dis_score=sum([compute_dis(poi,center) for poi in result if poi.head_class in keywords])
    #计算密度得分
    den_score_list=[head_class_counts[key] for key in head_class_counts.keys() if key in head_class]
    den_score=sum(den_score_list)
    #计算相关度得分
    if len(result) > 0:
        relevance_score = (0.4*dis_score/(len(dis_score_list) + 0.6*den_score/len(result) + 0.00001))*100
    else:
        relevance_score = 0  # 或其他你想赋予的默认值
    '''
    # 序列化结果为字典列表
    serialized_result = [
    {
        'id': poi.id,
        'name': poi.name,
        'head_class': poi.head_class,
        'small_class': poi.small_class,
        'lon': float(poi.lon),
        'lat': float(poi.lat)
    }
    for poi in result
    ]
    '''
    # 创建GeoJSON数据数组
    geojson_data = {
        'type': 'FeatureCollection',
        'features': [
            {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [float(poi.lon), float(poi.lat)]
            },
            'properties': {
                'id': poi.id,
                'name': poi.name,
                'head_class': poi.head_class,
                'small_class': poi.small_class
            }
        }
        for poi in selected_result
        ]
    }

    pois={
        'Code':200,
        'Msg':"成功返回数据",
        'totalNumber': len(geojson_data['features']),
        'poiData':geojson_data,
        'diversity_score':diversity_score,
        'relevance_score':relevance_score,
        'class_counts': head_class_counts,
    }
    return pois

if __name__ == '__main__':
    app.run(debug=True)