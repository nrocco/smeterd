__version__ = '2.0.0'
__description__ = '''Read smart meter P1 packets'''
__author__ = 'Nico Di Rocco'

if '__main__' == __name__:
    from smeterd.main import parse_and_run
    parse_and_run()
