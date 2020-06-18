def colorpalettable(name='morandi'):
    '''
    <name>: color
        'morandi': (default) morandi color list
        'macaron':
    '''
    from RZutilpy.figure import colormap

    # morandi list
    morandi_list=[
        '#a27e7e', '#c1cbd7', '#939391', '#c9c0d3', '#e0e5df', '#b5c4b1', '#8696a7', '#9ca8b8', '#ececea', '#fffaf4', '#96a48b', '#7b8b6f', '#965454', '#dfd7d7', '#656565', '#d8caaf', '#c5b8a5', '#fdf9ee', '#d3d4cc', '#e0cdcf', '#b7b1a5', '#a29988', '#dadad8', '#f8ebd8', '#afb0b2', '#6b5152', '#f0ebe5', '#cac3bb', '#a6a6a8', '#7a7281', '#ead0d1', '#faead3', '#c7b8a1', '#bfbfbf', '#eee5f8']

    # macaron list
    macaron_list=[
        '#f57e8b', '#ba9192', '#b5c07a', '#dd8270', '#bdcdbb',
        '#acb8b7', '#ddc9ac', '#6a4d5b', '#fff0a7', '#b09caa',
        '#a3b7b9', '#f6ebd8', '#f6d1b4', '#dab3a7', '#e0ce9f',
        '#3e1f16', '#940214', '#dd395a', '#e8c001', '#015c7a',
        '#98b7ac', '#cde0d7', '#fffcf1', '#f0e7da', '#d0c9c9',
        '#983b45', '#f7daae', '#f3eee4', '#86929f', '#222021']

    if name == 'morandi':
        return colormap(morandi_list, nColor=len(morandi_list))
    elif name == 'macaron':
        return colormap(macaron_list, nColor=len(macaron_list))
    else:
        raise ValueError('Only accept argument morandi and macaron')

