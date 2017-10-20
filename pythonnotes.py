#  ===== python command summary ==========
1. In ipython, rz.workefficiency.restart(), you can restart a kernel
2. sys.path to show all path
3. subprocess.run(['ls', '-al'])
4. intergers in numpy can not use elementwise negative power, should switch to float
    e.g., (np.arange(5)+1) ** (-3) report error
    e.g., (np.arange(5, dtype=float) + 1) ** (-3) is OK

# ======== Useful functions/tips ============
# 1. some times use map/zip/list together
# 2. np.split, np.reshape, np.vstack, np.hstack, np.dstack, np.concatenate
# 3. fix, ax = plt.subplots(3, 2, figsize=(12, 4))
# 4. plt.colorbar(pad=0.05, shrink=0.8)
# 5. repmat in matlab = np.tile
# 6. (A==B).all()
    np.array_equal(A,B)  # test if same shape, same elements values
    np.array_equiv(A,B)  # test if broadcastable shape, same elements values
    np.allclose(A,B,...) # test if same shape, elements have close enough values

# 8. remove extra axes,
     fig.delaxes(ax[-1])

# 9. get default colormap
plt.rcParams['axes.prop_cycle'].by_key()['color']
can get other cmap
plt.get_cmap('Set1', 20)

# 10. more efficient zip
    list(zip(x, y)) for y in ys

# 11. add a new axis
    ys = x[:50, np.newaxis]

# 12. np.tranpose is equal to permute in matlab

# 13.

# =========  String manipulation ==============
1. strcmp can use ==

matplotlib font
family: A list of font names in decreasing order of priority. The items may include a generic font family name, either ‘serif’, ‘sans-serif’, ‘cursive’, ‘fantasy’, or ‘monospace’. In that case, the actual font to be used will be looked up from the associated rcParam in matplotlibrc.
style: Either ‘normal’, ‘italic’ or ‘oblique’.
variant: Either ‘normal’ or ‘small-caps’.
stretch: A numeric value in the range 0-1000 or one of ‘ultra-condensed’, ‘extra-condensed’, ‘condensed’, ‘semi-condensed’, ‘normal’, ‘semi-expanded’, ‘expanded’, ‘extra-expanded’ or ‘ultra-expanded’
weight: A numeric value in the range 0-1000 or one of ‘ultralight’, ‘light’, ‘normal’, ‘regular’, ‘book’, ‘medium’, ‘roman’, ‘semibold’, ‘demibold’, ‘demi’, ‘bold’, ‘heavy’, ‘extra bold’, ‘black’
size: Either an relative value of ‘xx-small’, ‘x-small’, ‘small’, ‘medium’, ‘large’, ‘x-large’, ‘xx-large’ or an absolute font size, e.g., 12


# =========== matlibplot notes =========================
# 1.


# =========== pandas =============
# 1. delete a column or a
del data['aa']
data.drop([16 17])
data.drop([16 17], inplace=True)

# 2. find index based on a condition
a = df[(df.BoolCol == 3) & (df.attr == 22)].index.tolist()

# 3. find data based a condition
a = df[(df.BoolCol == 3) & (df.attr == 22)]



