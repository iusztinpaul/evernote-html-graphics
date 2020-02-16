import utils
import graphs
from parsers import HTMLMoneyDistributionParser

args = utils.get_program_args()
html_file_path = args.html_file_path

html_buffer = utils.get_data_from_html(html_file_path)

parser = HTMLMoneyDistributionParser(html_buffer)
parser.parse()

pie_chart = graphs.MoneyDistributionPieChart(parser.money_distribution)
pie_chart.plot()
