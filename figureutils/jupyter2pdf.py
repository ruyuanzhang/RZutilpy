def jupyter2pdf(jupyterFile, outputDir=None):
    '''
    convert jupyter2pdf using pdfkit.

    <jupyterFile>: a string or a Path-lib object

    <outputDir>: outputDir, default:cwd

    '''
    from RZutilpy.system import Path, makedirs
    import pdfkit

    jupyterFile = Path(jupyterFile)
    outputDir = Path.cwd() if outputDir is None else Path(outputDir)
    makedirs(outputDir) # create the dir if no exists

    name = jupyterFile.pstem

    !jupyter nbconvert --to html {name}

    htmlFile = Path(jupyterFile.strnosuffix+'.html')
    pdfkit.from_file(htmlFile.str, (outputDir/(name+'.pdf')).str)
    !rm -f {name}.html