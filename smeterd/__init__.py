VERSION = '1.6'
DESC = '''Read smart meter P1 packets'''


if '__main__' == __name__:
    from smeterd.main import parse_and_run
    parse_and_run()
