import logging
import subprocess
import json
from pyats import aetest

logger = logging.getLogger(__name__)

class tc_one(aetest.Testcase):

    @aetest.setup
    def prepare_testcase(self, section):
        logger.info("Preparing the test")
        logger.info(section)
        process_error = open('process_output_file.txt', 'w')
        process_stdout = open('output.json', 'w')
        client_process = subprocess.Popen(['iperf3', '-c', '172.22.35.18', '-J'], stdout=process_stdout, stderr = process_error)
        client_process.wait()
        process_error.close()
        process_stdout.close()

   ####################________________________###################################')


    @aetest.test
    def assert_test(self):
        logger.info('###########################________________________###################################')
        process_output_error_message = open('process_output_file.txt', 'r')
        if not process_output_error_message.readline():
            with open('output.json', 'r') as data_file:
                data = json.load(data_file)
                assert (data['end']['streams'][0]['receiver']['bytes'] / 1000000) > 40
                assert (data['end']['streams'][0]['receiver']['bits_per_second'] / 1000000) > 5
                process_output_error_message.close()
        
        else:
            process_output_error_message.close()
            process_output_error_message = open('process_output_file.txt', 'r')
            logger.info('###########################________________________###################################')
            logger.info(process_output_error_message.readline())
            logger.info('###########################________________________###################################')
            process_output_error_message.close()

    



    @aetest.cleanup
    def clean_testcase(self):
        logger.info("Pass testcase cleanup")

# if __name__ == '__main__': # pragma: no cover
#     aetest.main()

