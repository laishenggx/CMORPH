import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.colors as colors
import matplotlib as mpl
from dateutil.relativedelta import *
import datetime as dt

data_root='C:\\pyproject\\CMORPH\\data\\'

utc_time=dt.datetime(2019,3,20,0)
delta = relativedelta(hours=8)
bjt=utc_time+delta

file='surf_cli_chn_merge_cmp_pre_hour_grid_0.10SURF_CLI_CHN_MERGE_CMP_PRE_HOUR_GRID_0.10-%04d%02d%02d%02d.grd'\
     %(utc_time.year,utc_time.month,utc_time.day,utc_time.hour)
data=np.fromfile(data_root+file,dtype=np.float32)
data=data.reshape(2,440,700)
pre=np.maximum(data[0,:,:],0)

lon_leftup=70;lat_leftup=59
lon_rightdown=140;lat_rightdown=15
res=0.1
lon=np.arange(lon_leftup,lon_rightdown,res)
lat=np.arange(lat_rightdown,lat_leftup,res)
fig, ax = plt.subplots()
lon_leftup=70;lat_leftup=59
lon_rightdown=140;lat_rightdown=15
m = Basemap(projection='cyl', llcrnrlat=lat_rightdown, urcrnrlat=lat_leftup, llcrnrlon=lon_leftup, urcrnrlon=lon_rightdown, resolution='l')
m.readshapefile('C:\\dt\\bou2_4l', 'bou2_4l.shp', color='black',linewidth=0.3)
m.readshapefile('C:\\dt\\hyd1_4l', 'hyd1_4l', color=(0,120/255,1),linewidth=0.2)
m.drawcoastlines(linewidth=0.3, color='black')

parallels = np.arange(20,90,10) #纬线
m.drawparallels(parallels,labels=[True,False,False,False],linewidth=0.2,dashes=[1,4])
meridians = np.arange(0,200,10) #经线
m.drawmeridians(meridians,labels=[False,False,False,True],linewidth=0.2,dashes=[1,4])

cdict = [(151 / 255, 250 / 255, 151 / 255), (49/ 255, 204 / 255, 49/ 255), (126/ 255, 191 / 255, 237 / 255)
        , (0 / 255, 0 / 255, 255 / 255), (237/ 255, 0 / 255, 237 / 255)]
my_cmap = colors.ListedColormap(cdict,'pre3h')
my_cmap.set_under('w')
my_cmap.set_over((135/ 255, 25 / 255, 25 / 255))
lev=np.array([0.1,0.5,1,5,10,20])
norm3 = mpl.colors.BoundaryNorm(lev, my_cmap.N)

lons, lats = np.meshgrid(lon,lat)
x, y = m(lons, lats)
pp=m.contourf(x,y,pre,cmap=my_cmap,levels=lev,norm=norm3,extend='both')
cb=fig.colorbar(pp,ax=ax,pad=0.07,shrink=0.7,aspect=25,orientation='horizontal')
# cb=fig.colorbar(pp,ax=ax,pad=0.02,shrink=0.7,aspect=20)

font1={'family':'SimHei','size':8,'color':'b'}
font2={'family':'SimHei','size':8,'color':'k'}
font3={'family':'SimHei','size':8,'color':'r'}
ax.text(0.005, 1.02, '全国自动站&CMORPH降水融合产品:逐小时降水量(单位:mm)',fontdict=font2,transform=ax.transAxes)
ax.text(0.67, 1.06,'%04d年%02d月%02d日 %02d:00(北京时)'%(bjt.year,bjt.month,bjt.day,bjt.hour), transform=ax.transAxes, fontdict=font3)
ax.text(0.67, 1.015,'%04d年%02d月%02d日 %02d:00(世界时)'%(utc_time.year,utc_time.month,utc_time.day,utc_time.hour), transform=ax.transAxes, fontdict=font1)


#南海小图
a = plt.axes([0.753, 0.28, 0.12, 0.23])
lon_leftup=107;lat_leftup=24
lon_rightdown=121.3;lat_rightdown=2.4
m = Basemap(projection='cyl', llcrnrlat=lat_rightdown, urcrnrlat=lat_leftup, llcrnrlon=lon_leftup, urcrnrlon=lon_rightdown, resolution='l')
m.drawcoastlines(linewidth=0.3, color='gray')
m.contourf(x,y,pre,cmap=my_cmap,levels=lev,norm=norm3,extend='both')


m.readshapefile('C:\\dt\\bou2_4l', 'bou2_4l.shp', color='black',linewidth=0.3)
font1={'family':'SimHei','size':6,'color':'black'}
a.text(0.92,0.012,'南海诸岛',transform=ax.transAxes,fontdict=font1,bbox=dict(boxstyle='square',ec='k',fc='w',pad=0.3))
plt.savefig('%04d%02d%02d-%02d00.png'%(bjt.year,bjt.month,bjt.day,bjt.hour),dpi=300,bbox_inches='tight')
plt.show()