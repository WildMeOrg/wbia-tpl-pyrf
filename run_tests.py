#!/usr/bin/env python2.7
from __future__ import absolute_import, division, print_function
from os.path import join, split, exists
from pyrf import Random_Forest_Detector
import utool as ut


TEST_DATA_DETECT_URL = 'https://lev.cs.rpi.edu/public/data/testdata_detect.zip'
TEST_DATA_MODEL_URL = 'https://lev.cs.rpi.edu/public/models/rf.zip'


# Parallel code for resizing many images
def _resize_worker(gfpath, new_gfpath, new_size):
    """ worker function for parallel generator """
    import vtool as vt
    img = vt.imread(gfpath)
    new_img = vt.resize(img, new_size)
    vt.imwrite(new_gfpath, new_img)
    return new_gfpath


def resize_imagelist_generator(gpath_list, new_gpath_list, newsize_list, **kwargs):
    """ Resizes images and yeilds results asynchronously  """
    # Compute and write thumbnail in asychronous process
    kwargs['force_serial'] = kwargs.get('force_serial', True)
    kwargs['ordered']      = kwargs.get('ordered', True)
    arg_iter = zip(gpath_list, new_gpath_list, newsize_list)
    arg_list = list(arg_iter)
    return ut.generate2(_resize_worker, arg_list, **kwargs)


def resize_imagelist_to_sqrtarea(gpath_list, new_gpath_list=None,
                                 sqrt_area=800, output_dir=None,
                                 checkexists=True,
                                 **kwargs):
    """ Resizes images and yeilds results asynchronously  """
    import vtool as vt
    target_area = sqrt_area ** 2
    # Read image sizes
    gsize_list = [vt.open_image_size(gpath) for gpath in gpath_list]
    # Compute new sizes which preserve aspect ratio
    newsize_list = [vt.ScaleStrat.area(target_area, wh) for wh in gsize_list]
    if new_gpath_list is None:
        # Compute names for the new images if not given
        if output_dir is None:
            # Create an output directory if not specified
            output_dir      = 'resized_sqrtarea%r' % sqrt_area
        ut.ensuredir(output_dir)
        size_suffixs =  ['_' + repr(newsize).replace(' ', '') for newsize in newsize_list]
        from os.path import basename
        old_gnames = [basename(p) for p in gpath_list]
        new_gname_list = [ut.augpath(p, suffix=s)
                          for p, s in zip(old_gnames, size_suffixs)]
        new_gpath_list = [join(output_dir, gname) for gname in new_gname_list]
        new_gpath_list = list(map(ut.unixpath, new_gpath_list))
    assert len(new_gpath_list) == len(gpath_list), 'unequal len'
    assert len(newsize_list) == len(gpath_list), 'unequal len'
    # Evaluate generator
    if checkexists:
        exists_list = list(map(exists, new_gpath_list))
        gpath_list_ = ut.filterfalse_items(gpath_list, exists_list)
        new_gpath_list_ = ut.filterfalse_items(new_gpath_list, exists_list)
        newsize_list_ = ut.filterfalse_items(newsize_list, exists_list)
    else:
        gpath_list_ = gpath_list
        new_gpath_list_ = new_gpath_list
        newsize_list_ = newsize_list
    generator = resize_imagelist_generator(gpath_list_, new_gpath_list_,
                                           newsize_list_, **kwargs)
    for res in generator:
        pass
    #return [res for res in generator]
    return new_gpath_list


def test_pyrf():
    r"""
    CommandLine:
        python run_tests.py --test-test_pyrf

    Example:
        >>> # ENABLE_DOCTEST
        >>> from run_tests import *  # NOQA
        >>> result = test_pyrf()
        >>> print(result)
    """

    #=================================
    # Initialization
    #=================================

    category = 'zebra_plains'

    #detect_config = {
    #    'save_detection_images':        True,
    #    'percentage_top':               0.40,
    #}

    testdata_dir = ut.unixpath('~/code/pyrf/results')
    # assert ut.checkpath(testdata_dir)
    if ut.get_argflag('--vd'):
        print(ut.ls(testdata_dir))

    # Create detector
    detector = Random_Forest_Detector()

    test_path = ut.grab_zipped_url(TEST_DATA_DETECT_URL, appname='utool')
    models_path = ut.grab_zipped_url(TEST_DATA_MODEL_URL, appname='utool')
    trees_path = join(models_path, category)
    detect_path = join(test_path, category, 'detect')
    ut.ensuredir(detect_path)
    ut.ensuredir(test_path)
    ut.ensuredir(trees_path)

    #=================================
    # Load Input Images
    #=================================

    # Get input images
    big_gpath_list = ut.list_images(test_path, fullpath=True, recursive=False)
    print(big_gpath_list)
    # Resize images to standard size
    if ut.get_argflag('--small'):
        big_gpath_list = big_gpath_list[0:8]
    #big_gpath_list = big_gpath_list[0:8]
    output_dir = join(test_path, 'resized')
    std_gpath_list = resize_imagelist_to_sqrtarea(big_gpath_list,
                                                  sqrt_area=800,
                                                  output_dir=output_dir,
                                                  checkexists=True)
    dst_gpath_list = [join(detect_path, split(gpath)[1]) for gpath in std_gpath_list]
    #ut.view_directory(test_path)
    #ut.view_directory('.')
    print(std_gpath_list)
    num_images = len(std_gpath_list)
    #assert num_images == 16, 'the test has diverged!'
    print('Testing on %r images' % num_images)

    #=================================
    # Load Pretrained Forests
    #=================================

    # Load forest, so we don't have to reload every time
    trees_fpath_list = ut.ls(trees_path, '*.txt')
    #forest = detector.load(trees_path, category + '-')
    forest = detector.forest(trees_fpath_list)
    #detector.set_detect_params(**detect_config)
    results_list1 = []

    #=================================
    # Detect using Random Forest
    #=================================

    with ut.Timer('[test_pyrf] for loop detector.detect') as t1:
        if not ut.get_argflag('--skip1'):
            results_list1 = detector.detect(forest, std_gpath_list, output_gpath_list=dst_gpath_list)
            #for ix, (img_fpath, dst_fpath) in enumerate(zip(std_gpath_list, dst_gpath_list)):
            #    #img_fname = split(img_fpath)[1]
            #    #dst_fpath = join(detect_path, img_fname)
            #    #print('  * img_fpath = %r' % img_fpath)
            #    #print('  * dst_fpath = %r' % dst_fpath)
            #    with ut.Timer('[test_pyrf] detector.detect ix=%r' % (ix,)):
            #        results = detector.detect(forest, img_fpath, dst_fpath)
            #    results_list1.append(results)
            #    print('num results = %r' % len(results))
            #else:
            #    print('...skipped')

    #with ut.Timer('[test_pyrf] detector.detect_many') as t2:
    #    results_list2 = detector.detect_many(forest, std_gpath_list,
    #                                         dst_gpath_list, use_openmp=True)
    detector.free_forest(forest)

    print('')
    print('+ --------------')
    print('| total time1: %r' % t1.ellapsed)
    #print('| total time2: %r' % t2.ellapsed)
    print('|')
    print('| num results1 = %r' % (list(map(len, results_list1))))
    #print('| num results2 = %r' % (list(map(len, results_list2))))
    #assert results_list2 == results_list1
    return locals()


if __name__ == '__main__':
    r"""
    CommandLine:
        export PYTHONPATH=$PYTHONPATH:/home/joncrall/code/pyrf
        python ~/code/pyrf/run_tests.py
        python ~/code/pyrf/run_tests.py --allexamples
    """
    import multiprocessing
    multiprocessing.freeze_support()  # for win32
    import utool as ut  # NOQA
    ut.doctest_funcs()
