# evaluate 2d polyfit
x = np.arange(10.)
y = -5 - x + 3*x**2
m[2]=np.nan  # note that nan is float data type, when given value, set the
# matrix dtype to float

coef, predy, resi = rz.stats.polyfit1d(x, y, deg=2)

plt.close('all')
plt.scatter(y, predy)

# evaluate 2d polyfit
x, y = np.arange(10.), np.arange(10.)
xx,yy = np.meshgrid(x, y)
m = -5 + 3*yy**2 + xx - 4*xx**2
m[:,2]=np.nan  # note that nan is float data type, when given value, set the
# matrix dtype to float

coef, predm, _ , _ = rz.stats.polyfit2d(x, y, m, deg=2)

plt.close('all')
plt.subplot(131)
plt.imshow(m)
plt.subplot(132)
plt.imshow(predm)
plt.subplot(133)
plt.scatter(m, predm)



# evaluate 3d polyfit
x, y, z = np.arange(10.), np.arange(10.), np.arange(10.)
xx,yy,zz = np.meshgrid(x, y, z)
m = -5 + 3*yy**2 + xx - 4*xx**2 - zz**2
m[:,2,5]=np.nan  # note that nan is float data type, when given value, set the
# matrix dtype to float

coef, predm, _ , _ = rz.stats.polyfit3d(x, y, z, m, deg=2)

plt.close('all')
plt.subplot(131)
plt.imshow(rz.imageprocess.makeimagestack(m))
plt.subplot(132)
plt.imshow(rz.imageprocess.makeimagestack(predm))
plt.subplot(133)
plt.scatter(m, predm)
