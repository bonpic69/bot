import os
import json
import configparser
import pyfiglet
from colorama import init, Fore
import time
import datetime
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from re import search
from threading import Thread
from telethon import TelegramClient, events, sync
import sys
from threading import RLock

lock = RLock()
init()

lg = Fore.LIGHTGREEN_EX
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
r = Fore.RED
n = Fore.RESET
colors = [lg, r, w, cy, ye]
positions = {}


# common functions
def get_timestamp():
    return int(time.time() * 1000)


def get_current_date_time():
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")


def append_to_txt_file(json_object, file_name):
    with open(file_name, 'a') as outfile:
        outfile.write(str(get_current_date_time()) +
                      ' ' + str(json_object) + '\n')


# init functions
def get_config_object():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config_object = {
        'rgb_id': config.get('API', 'rgb_id'),
        'rgb_id_app': config.get('API', 'rgb_id_app'),
        'moon_bag': config.get('API', 'moon_bag'),
        ## LIVE keys
        'rgb_id_cht': config.get('API', 'rgb_id_cht'),  # VIP Channel
        'bg_id': config.get('API', 'bg_id'),  # live keys
        'bg_id_k': config.get('API', 'bg_id_k'),
        'bs_pi': config.get('API', 'bs_pi'),
        'pos_sz': config.get('API', 'pos_sz'),
        'sl_prc': str(float(config.get('API', 'sl_prc')) / 10.0),
        'tp_no': '6',
        'lev': config.get('API', 'lev'),
        'trailing_sl': config.get('API', 'trailing_sl')
    }
    clr()
    banner()
    print('\n')
    print('\n')
    print(lg + get_current_date_time() +
          ' Bot started!' + n + '\n')
    print(lg + get_current_date_time() +
          ' Entering positions with ' + str(config_object['pos_sz']) + "% of Account Balance and Stop Loss: "
          + str(float(config_object['sl_prc']) * 10.0) + "% " + n + '\n')
    return config_object


def banner():
    f = pyfiglet.Figlet(font='slant')
    b = f.renderText("BINANCE FUTURES BOT")
    print(f'{w}{b}{n}')


def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


# binance functions
def get_decimals_precision(number):
    if str(number).__contains__("."):
        return str(str(number).index('1') - 1)
    else:
        return str(number)


def convert_to_precision(precision_number, number):
    if str(number).__contains__("."):
        decimals = str(number).split('.')[1]
        final_string = ''
        if len(decimals) >= precision_number:
            if precision_number == 1:
                final_string = int(str(number).split('.')[0])
                return float(final_string)
            elif precision_number == 2:
                final_string += list(decimals)[0]
                final_string += list(decimals)[1]
                return float(str(number).split('.')[0] + '.' + final_string)
            elif precision_number == 3:
                final_string += list(decimals)[0]
                final_string += list(decimals)[1]
                final_string += list(decimals)[2]
                return float(str(number).split('.')[0] + '.' + final_string)
            elif precision_number == 4:
                final_string += list(decimals)[0]
                final_string += list(decimals)[1]
                final_string += list(decimals)[2]
                final_string += list(decimals)[3]
                return float(str(number).split('.')[0] + '.' + final_string)
            elif precision_number == 5:
                final_string += list(decimals)[0]
                final_string += list(decimals)[1]
                final_string += list(decimals)[2]
                final_string += list(decimals)[3]
                final_string += list(decimals)[4]
                return float(str(number).split('.')[0] + '.' + final_string)
            elif precision_number == 6:
                final_string += list(decimals)[0]
                final_string += list(decimals)[1]
                final_string += list(decimals)[2]
                final_string += list(decimals)[3]
                final_string += list(decimals)[4]
                final_string += list(decimals)[5]
                return float(str(number).split('.')[0] + '.' + final_string)
            elif precision_number == 7:
                final_string += list(decimals)[0]
                final_string += list(decimals)[1]
                final_string += list(decimals)[2]
                final_string += list(decimals)[3]
                final_string += list(decimals)[4]
                final_string += list(decimals)[5]
                final_string += list(decimals)[6]
                return float(str(number).split('.')[0] + '.' + final_string)
            elif precision_number == 8:
                final_string += list(decimals)[0]
                final_string += list(decimals)[1]
                final_string += list(decimals)[2]
                final_string += list(decimals)[3]
                final_string += list(decimals)[4]
                final_string += list(decimals)[5]
                final_string += list(decimals)[6]
                final_string += list(decimals)[7]
                return float(str(number).split('.')[0] + '.' + final_string)
            elif precision_number == 9:
                final_string += list(decimals)[0]
                final_string += list(decimals)[1]
                final_string += list(decimals)[2]
                final_string += list(decimals)[3]
                final_string += list(decimals)[4]
                final_string += list(decimals)[5]
                final_string += list(decimals)[6]
                final_string += list(decimals)[7]
                final_string += list(decimals)[8]
                return float(str(number).split('.')[0] + '.' + final_string)
            elif precision_number == 10:
                final_string += list(decimals)[0]
                final_string += list(decimals)[1]
                final_string += list(decimals)[2]
                final_string += list(decimals)[3]
                final_string += list(decimals)[4]
                final_string += list(decimals)[5]
                final_string += list(decimals)[6]
                final_string += list(decimals)[7]
                final_string += list(decimals)[8]
                final_string += list(decimals)[9]
                return float(str(number).split('.')[0] + '.' + final_string)
        else:
            return float(number)


def check_exit_points(string, tp_no):
    exit_points = []
    if tp_no == '1':
        if search('1\)', string) and search('2\)', string):
            exit_points.append(string.split('1)')[1].split('2)')[0].strip())
    elif tp_no == '2':
        if search('1\)', string) and search('2\)', string):
            exit_points.append(string.split('1)')[1].split('2)')[0].strip())
        if search('2\)', string) and search('3\)', string):
            exit_points.append(string.split('2)')[1].split('3)')[0].strip())
    elif tp_no == '3':
        if search('1\)', string) and search('2\)', string):
            exit_points.append(string.split('1)')[1].split('2)')[0].strip())
        if search('2\)', string) and search('3\)', string):
            exit_points.append(string.split('2)')[1].split('3)')[0].strip())
        if search('3\)', string) and search('4\)', string):
            exit_points.append(string.split('3)')[1].split('4)')[0].strip())
    elif tp_no == '4':
        if search('1\)', string) and search('2\)', string):
            exit_points.append(string.split('1)')[1].split('2)')[0].strip())
        if search('2\)', string) and search('3\)', string):
            exit_points.append(string.split('2)')[1].split('3)')[0].strip())
        if search('3\)', string) and search('4\)', string):
            exit_points.append(string.split('3)')[1].split('4)')[0].strip())
        if search('4\)', string) and search('5\)', string):
            exit_points.append(string.split('4)')[1].split('5)')[0].strip())
    elif tp_no == '5':
        if search('1\)', string) and search('2\)', string):
            exit_points.append(string.split('1)')[1].split('2)')[0].strip())
        if search('2\)', string) and search('3\)', string):
            exit_points.append(string.split('2)')[1].split('3)')[0].strip())
        if search('3\)', string) and search('4\)', string):
            exit_points.append(string.split('3)')[1].split('4)')[0].strip())
        if search('4\)', string) and search('5\)', string):
            exit_points.append(string.split('4)')[1].split('5)')[0].strip())
        if search('5\)', string) and search('6\)', string):
            exit_points.append(string.split('5)')[1].split('6)')[0].strip())
    elif tp_no == '6':
        if search('1\)', string) and search('2\)', string):
            exit_points.append(string.split('1)')[1].split('2)')[0].strip())
        if search('2\)', string) and search('3\)', string):
            exit_points.append(string.split('2)')[1].split('3)')[0].strip())
        if search('3\)', string) and search('4\)', string):
            exit_points.append(string.split('3)')[1].split('4)')[0].strip())
        if search('4\)', string) and search('5\)', string):
            exit_points.append(string.split('4)')[1].split('5)')[0].strip())
        if search('5\)', string) and search('6\)', string):
            exit_points.append(string.split('5)')[1].split('6)')[0].strip())
        if search('6\)', string) and search('7\)', string):
            exit_points.append(string.split('6)')[1].split('7)')[0].strip())
    elif tp_no == '7':
        if search('1\)', string) and search('2\)', string):
            exit_points.append(string.split('1)')[1].split('2)')[0].strip())
        if search('2\)', string) and search('3\)', string):
            exit_points.append(string.split('2)')[1].split('3)')[0].strip())
        if search('3\)', string) and search('4\)', string):
            exit_points.append(string.split('3)')[1].split('4)')[0].strip())
        if search('4\)', string) and search('5\)', string):
            exit_points.append(string.split('4)')[1].split('5)')[0].strip())
        if search('5\)', string) and search('6\)', string):
            exit_points.append(string.split('5)')[1].split('6)')[0].strip())
        if search('6\)', string) and search('7\)', string):
            exit_points.append(string.split('6)')[1].split('7)')[0].strip())
        if search('7\)', string) and search('8\)', string):
            exit_points.append(string.split('7)')[1].split('8)')[0].strip())
    # Adding 2 more TPs
    if search('6\)', string) and search('7\)', string):
        tp1 = float(string.split('5)')[1].split('6)')[0].strip())
        tp2 = float(string.split('6)')[1].split('7)')[0].strip())
        if tp1 < tp2:  # Long order
            tp7 = tp2 + (tp2 * (2.50 / 100.0))
            tp8 = tp2 + (tp2 * (5.00 / 100.0))
        else:  # Short order
            tp7 = tp2 - (tp2 * (2.50 / 100.0))
            tp8 = tp2 - (tp2 * (5.00 / 100.0))
        exit_points.append(str(tp7))
        exit_points.append(str(tp8))
    return exit_points


def get_exchange_info(config_object, base_api, endpoint):
    return send_public_request(config_object, base_api, endpoint)


def place_position_and_orders_futures(signal, config_object):
    global positions
    moon_bag = config_object['moon_bag']
    tp = []
    sl = []
    tp_temp = []
    account_balance_response = send_signed_request(
        config_object, 'GET', config_object['bs_pi'], '/fapi/v2/balance')
    USDT_balance = float(list(
        filter(lambda x: x['asset'] == 'USDT', account_balance_response))[0]['balance'])
    print(lg + get_current_date_time() +
          ' Your USDT balance is: ' + str(USDT_balance) + n + '\n')
    pos_size = USDT_balance * (float(config_object['pos_sz']) / 100.0) # Percentage of deposit
    if USDT_balance >= pos_size :
        exchange_info = get_exchange_info(
            config_object, config_object['bs_pi'], '/fapi/v1/exchangeInfo')
        tick_size_number_of_decimals = int(get_decimals_precision(
            list(filter(lambda x: x['symbol'] == signal['SYMBOL'], exchange_info['symbols']))[0]['filters'][0][
                'tickSize']))
        min_qty_number_of_decimals = int(get_decimals_precision(
            list(filter(lambda x: x['symbol'] == signal['SYMBOL'], exchange_info['symbols']))[0]['filters'][1][
                'minQty']))
        leverage_params = {
            "symbol": signal['SYMBOL'],
            "leverage": config_object['lev'] if config_object['lev'] else signal['LEVERAGE'],
        }
        change_leverage_response = send_signed_request(
            config_object, 'POST', config_object['bs_pi'], '/fapi/v1/leverage', leverage_params)
        if 'msg' in change_leverage_response:
            print(r + get_current_date_time() + ' New error occurred: ' + str(
                change_leverage_response['msg']) + n + '\n')
        else:
            print(lg + get_current_date_time() +
                  ' Changed leverage successfully with: ' + str(change_leverage_response['leverage']) + n + '\n')
        change_margin_response = send_signed_request(
            config_object, 'POST', config_object['bs_pi'], '/fapi/v1/marginType',
            {'symbol': signal['SYMBOL'], 'marginType': 'CROSSED'})
        print(lg + get_current_date_time() +
              ' Changed margin successfully with: CROSS' + n + '\n')
        # Check for existing position of same Symbol
        pos_adj = 0.0
        check_pos = send_signed_request(
            config_object, 'GET', config_object['bs_pi'], '/fapi/v2/positionRisk', {"symbol": signal['SYMBOL']})
        if len(check_pos) > 0 and 'msg' not in check_pos:  # there is an active position of same symbol
            # active long position and short trade to open
            if float(check_pos[0]['positionAmt']) > 0.0 and signal['TRADE_TYPE'] == 'Short':
                print(lg + get_current_date_time() + " Long position active" + n + '\n')
                pos_adj = abs(float(check_pos[0]['positionAmt']))
                if signal['SYMBOL'] in positions:
                    sl_id = positions[signal['SYMBOL']][0]
                    if len(sl_id) > 0:
                        sl_cancel_response = send_signed_request(
                            config_object, 'DELETE', config_object['bs_pi'], '/fapi/v1/order',
                            {'symbol': signal['SYMBOL'], 'orderId': sl_id[0]})
                        print(lg + get_current_date_time() + ' Close SL Order... \n')
                        append_to_txt_file(sl_cancel_response,
                                           'positions_and_orders.txt')
                        print(lg + get_current_date_time() +
                              ' SL order cancelled. ' + n + '\n')
            # active short position and long trade to open
            elif float(check_pos[0]['positionAmt']) < 0.0 and signal['TRADE_TYPE'] == 'Long':
                print(lg + get_current_date_time() + " Short position active" + n + '\n')
                pos_adj = abs(float(check_pos[0]['positionAmt']))
                sl_id = positions[signal['SYMBOL']][0]
                if len(sl_id) > 0:
                    sl_cancel_response = send_signed_request(
                        config_object, 'DELETE', config_object['bs_pi'], '/fapi/v1/order',
                        {'symbol': signal['SYMBOL'], 'orderId': sl_id[0]})
                    print(lg + get_current_date_time() + ' Close SL Order... \n')
                    append_to_txt_file(sl_cancel_response,
                                       'positions_and_orders.txt')
                    print(lg + get_current_date_time() +
                          ' SL order canceled. ' + n + '\n')
            elif abs(float(check_pos[0]['positionAmt'])) > 0.0:  # Same side order, modify SL
                sl_id = positions[signal['SYMBOL']][0]
                if len(sl_id) > 0:
                    sl_cancel_response = send_signed_request(
                        config_object, 'DELETE', config_object['bs_pi'], '/fapi/v1/order',
                        {'symbol': signal['SYMBOL'], 'orderId': sl_id[0]})
                    print(lg + get_current_date_time() + ' Close SL Order... \n')
                    append_to_txt_file(sl_cancel_response,
                                       'positions_and_orders.txt')
                    print(lg + get_current_date_time() +
                          ' SL order canceled ' + n + '\n')
                tp_temp = positions[signal['SYMBOL']][1]
        open_position = {
            "symbol": signal['SYMBOL'],
            "side": 'SELL' if signal['TRADE_TYPE'] == 'Short' else 'BUY',
            "type": "MARKET",
            "quantity": str(convert_to_precision(min_qty_number_of_decimals,
                                                 pos_adj + pos_size * float(
                                                     change_leverage_response['leverage']) / float(
                                                     signal['ENTRY_POINT']))),
            "workingType": 'MARK_PRICE'
        }
        open_position_response = send_signed_request(
            config_object, 'POST', config_object['bs_pi'], '/fapi/v1/order', open_position)
        append_to_txt_file(open_position_response, 'positions_and_orders.txt')

        if 'msg' in open_position_response:
            print(r + get_current_date_time() + ' New error occurred: ' + str(
                open_position_response['msg']) + n + '\n')
        else:
            print(lg + get_current_date_time() + " " +
                  signal['TRADE_TYPE'] + ' position opened for ' + signal['SYMBOL']
                  + ' with Pos size: ' + str(round(pos_size, 2)) + n + '\n')
            if float(float(config_object['sl_prc'])) != float('0'):
                target_price_long = str(convert_to_precision(tick_size_number_of_decimals, float(
                    float(convert_to_precision(tick_size_number_of_decimals,
                                               convert_to_precision(tick_size_number_of_decimals, float(
                                                   send_signed_request(config_object, 'GET', config_object['bs_pi'],
                                                                       '/fapi/v1/ticker/24hr',
                                                                       {'symbol': signal['SYMBOL']})[
                                                       'lastPrice'])))) * (float(config_object['sl_prc']) / float(
                        leverage_params['leverage']) + 1))))
                target_price_short = str(convert_to_precision(tick_size_number_of_decimals, float(
                    float(convert_to_precision(tick_size_number_of_decimals,
                                               convert_to_precision(tick_size_number_of_decimals, float(
                                                   send_signed_request(config_object, 'GET', config_object['bs_pi'],
                                                                       '/fapi/v1/ticker/24hr',
                                                                       {'symbol': signal['SYMBOL']})[
                                                       'lastPrice'])))) * (1 - float(config_object['sl_prc']) / float(
                        leverage_params['leverage'])))))
                stop_loss = {
                    "symbol": signal['SYMBOL'],
                    "side": 'BUY' if signal['TRADE_TYPE'] == 'Short' else 'SELL',
                    "type": "STOP_MARKET",
                    "stopPrice": target_price_long if signal['TRADE_TYPE'] == 'Short' else target_price_short,
                    "closePosition": 'true',
                    "timeInForce": "GTE_GTC",
                    "workingType": 'MARK_PRICE'
                }
                stop_loss_order = send_signed_request(config_object, 'POST', config_object['bs_pi'],
                                                      '/fapi/v1/order',
                                                      stop_loss)
                append_to_txt_file(stop_loss_order, 'positions_and_orders.txt')
                print(lg + get_current_date_time() +
                      ' Stop Loss added. ' + n + '\n')
                if 'msg' not in stop_loss_order:
                    sl.append(stop_loss_order['orderId'])

            # check if quantity is not zero
            tp_quantity = convert_to_precision(min_qty_number_of_decimals,
                                               (float(open_position_response['origQty']) - pos_adj) / float(
                                                   len(signal['EXIT_POINTS'])))
            if tp_quantity == 0:  # only one TP
                exit_point = signal['EXIT_POINTS'][-1]
                take_profit = {
                    "symbol": signal['SYMBOL'],
                    "side": 'BUY' if signal['TRADE_TYPE'] == 'Short' else 'SELL',
                    "type": 'TAKE_PROFIT_MARKET',
                    "quantity": str(convert_to_precision(min_qty_number_of_decimals,
                                                         float(open_position_response['origQty']) - pos_adj)),
                    "stopPrice": str(convert_to_precision(tick_size_number_of_decimals, float(exit_point))),
                    "timeInForce": "GTE_GTC",
                    "closePosition": 'false',
                    "workingType": 'MARK_PRICE'
                }
                new_take_profit_order = send_signed_request(config_object, 'POST',
                                                            config_object['bs_pi'], '/fapi/v1/order',
                                                            take_profit)
                append_to_txt_file(new_take_profit_order,
                                   'positions_and_orders.txt')
                print(lg + get_current_date_time() +
                      '  1 Take Profit order created. ' + n + '\n')
                if not tp:
                    tp.append(1)  # only one tp order
                if 'msg' not in new_take_profit_order:
                    tp.append(new_take_profit_order['orderId'])
                else:
                    tp.append('')
            else:
                if not tp:
                    tp.append(len(signal['EXIT_POINTS'][:-1]))
                if moon_bag == 'True':
                    tps = signal['EXIT_POINTS'][:-1]
                else:
                    tps = signal['EXIT_POINTS']
                count = 1
                for exit_point in tps:  # skipping last TP if moon bag
                    take_profit = {
                        "symbol": signal['SYMBOL'],
                        "side": 'BUY' if signal['TRADE_TYPE'] == 'Short' else 'SELL',
                        "type": 'TAKE_PROFIT_MARKET',
                        "quantity": str(tp_quantity),
                        "stopPrice": str(convert_to_precision(tick_size_number_of_decimals, float(exit_point))),
                        "timeInForce": "GTE_GTC",
                        "closePosition": 'false',
                        "workingType": 'MARK_PRICE'
                    }
                    new_take_profit_order = send_signed_request(config_object, 'POST',
                                                                config_object['bs_pi'], '/fapi/v1/order',
                                                                take_profit)
                    append_to_txt_file(new_take_profit_order,
                                       'positions_and_orders.txt')
                    print(lg + get_current_date_time() + " " + str(count) +
                          ' Take Profit order created. ' + n + '\n')
                    count += 1
                    if 'msg' not in new_take_profit_order:
                        tp.append(new_take_profit_order['orderId'])
                    else:
                        tp.append('')
            if tp_temp is not []:
                tp = tp + tp_temp[1:]
            with lock:
                positions.update({signal['SYMBOL']: [sl, tp]})
    else:
        print(r + get_current_date_time() +
              ' Your account balance is too low, please add funds!' + n + '\n')


def check_live_open_orders(config_object, symbol, open_orders_response):
    global positions
    tp = []
    sl = []
    current_symbol_open_orders = list(
        filter(lambda x: x['symbol'] == symbol, open_orders_response))
    current_stop_limit_order = list(
        filter(lambda x: x['origType'] == 'STOP_MARKET', current_symbol_open_orders))
    current_trailing_stop_order = list(
        filter(lambda x: x['origType'] == 'TRAILING_STOP_MARKET', current_symbol_open_orders))
    current_take_profit_orders = list(
        filter(lambda x: x['origType'] == 'TAKE_PROFIT_MARKET', current_symbol_open_orders))
    print(lg + get_current_date_time() + ' Available Stop Limit order for' +
          ' ' + symbol + ' ' + str(len(current_stop_limit_order)) + n + '\n')
    print(lg + get_current_date_time() + ' Available Trailing Stop order for' +
          ' ' + symbol + ' ' + str(len(current_trailing_stop_order)) + n + '\n')
    print(lg + get_current_date_time() + ' Available Take Profit orders for' +
          ' ' + symbol + ' ' + str(len(current_take_profit_orders)) + n + '\n')
    if len(current_take_profit_orders) == 0 and len(current_stop_limit_order) == 0:
        tp = [1, ""]
    elif len(current_take_profit_orders) == 0 and len(current_stop_limit_order) > 0:
        tp = [0, ""]
    elif len(current_take_profit_orders) > 0:
        tp = [len(current_take_profit_orders)] + [tp['orderId'] for tp in current_take_profit_orders]
    if len(current_stop_limit_order) == 0 and current_trailing_stop_order == 0:
        sl = []
    elif len(current_trailing_stop_order) > 0:
        sl = [sl['orderId'] for sl in current_trailing_stop_order]
    elif len(current_stop_limit_order) > 0:
        sl = [sl['orderId'] for sl in current_stop_limit_order]
    positions.update({symbol: [sl, tp]})



def sync_positions(config_object):
    global positions
    moon_bag = config_object['moon_bag']
    # Go through all positions check if they are active or else delete entries from the dict
    while True:
        check_open_pos_filt = []
        check_open_pos = []
        tps = []
        sl = []
        print(cy + get_current_date_time() +
              ' Positions updated... \n')
        exchange_info = get_exchange_info(
            config_object, config_object['bs_pi'], '/fapi/v1/exchangeInfo')
        check_pos_list = send_signed_request(
            config_object, 'GET', config_object['bs_pi'], '/fapi/v2/positionRisk')
        check_open_pos = send_signed_request(
            config_object, 'GET', config_object['bs_pi'], '/fapi/v1/openOrders')
        if len(check_pos_list) > 0 and 'msg' not in check_pos_list:
            check_pos_filt = [[check_pos['symbol'], check_pos['positionAmt'], check_pos['entryPrice']] for check_pos in
                              check_pos_list if
                              abs(float(check_pos['positionAmt'])) > 0]
        if len(check_open_pos) > 0 and 'msg' not in check_open_pos:
            check_open_pos_filt = [check_pos['orderId'] for check_pos in check_open_pos]
        with lock:
            temp_pos = positions.copy()
        for key, value in temp_pos.items():
            tick_size_number_of_decimals = int(get_decimals_precision(
                list(filter(lambda x: x['symbol'] == key, exchange_info['symbols']))[0]['filters'][0][
                    'tickSize']))
            # active long position and short trade to open
            if key in [pos[0] for pos in check_pos_filt]:  # there is an active position for symbol
                tps = value[1]
                sl = value[0]
                if len(sl) > 0: # We have stop loss
                    if sl[0] not in check_open_pos_filt:
                        sl = []
                        value[0] = sl
                        with lock:
                            positions[key] = value
                else:
                    sl = []
                    value[0] = sl
                    with lock:
                        positions[key] = value
                if tps[0] != 0:  # we have TPs
                    tps_filt = tps[1:]
                    empty_tps = [l for l in tps_filt if isinstance(l, str)]
                    # Check if there are any existing TPs
                    if len(tps_filt) > len(empty_tps):  # We have existing tp's
                        for i in range(0, len(tps_filt)):
                            if tps_filt[i] != '':
                                # Check if all TP's are open or already hit
                                if tps_filt[i] not in check_open_pos_filt:
                                    tps_filt[i] = ''
                        value[1] = [tps[0]] + tps_filt
                        with lock:
                            positions[key] = value
                    elif len(tps_filt) == len(empty_tps) and moon_bag == 'True':  # We have hit all TP's and moonbag modify SL
                        if len(value[0]) > 0:
                            sl_cancel_response = send_signed_request(
                                config_object, 'DELETE', config_object['bs_pi'], '/fapi/v1/order',
                                {'symbol': key, 'orderId': value[0][0]})
                            if 'msg' not in sl_cancel_response:
                                append_to_txt_file(sl_cancel_response,
                                                   'positions_and_orders.txt')
                                print(lg + get_current_date_time() +
                                      ' SL order canceled. ' + n + '\n')
                                if config_object['trailing_sl'] == 'True':
                                    exchange_info = get_exchange_info(
                                        config_object, config_object['bs_pi'], '/fapi/v1/exchangeInfo')
                                    min_qty_number_of_decimals = int(get_decimals_precision(
                                        list(filter(lambda x: x['symbol'] == key,
                                                    exchange_info['symbols']))[0]['filters'][1][
                                            'minQty']))
                                    entry_price = float(convert_to_precision(tick_size_number_of_decimals,
                                                                              check_pos_filt[[pos[0] for pos in
                                                                                              check_pos_filt].index(
                                                                                  key)][2]))
                                    check_pos_list = send_signed_request(
                                        config_object, 'GET', config_object['bs_pi'], '/fapi/v2/positionRisk')
                                    trail_order = [check_pos for check_pos in check_pos_list if
                                               abs(float(check_pos['positionAmt'])) > 0 and key in check_pos['symbol']][0]
                                    quantity = str(convert_to_precision(min_qty_number_of_decimals,
                                                 abs(float(trail_order['positionAmt']))))
                                    stop_loss = {
                                        "symbol": key,
                                        "orderId": value[0][0],
                                        "side": 'SELL' if float(check_pos_filt[[pos[0]
                                                                                for pos in check_pos_filt].index(key)][
                                                                    1]) > 0.0 else 'BUY',
                                        "type": "TRAILING_STOP_MARKET",
                                        "quantity": quantity,
                                        "timeInForce": "GTE_GTC",
                                        "workingType": 'CONTRACT_PRICE',
                                        "callbackRate": '5'
                                    }
                                else:
                                    stop_loss = {
                                        "symbol": key,
                                        "orderId": value[0][0],
                                        "side": 'SELL' if float(check_pos_filt[[pos[0]
                                                                                for pos in check_pos_filt].index(key)][
                                                                    1]) > 0.0 else 'BUY',
                                        "type": "STOP_MARKET",
                                        "stopPrice": str(convert_to_precision(tick_size_number_of_decimals,
                                                                              check_pos_filt[[pos[0] for pos in check_pos_filt].index(key)][2])),
                                        #
                                        "closePosition": 'true',
                                        "timeInForce": "GTE_GTC",
                                        "workingType": 'MARK_PRICE'
                                    }
                                stop_loss_order = send_signed_request(config_object, 'POST', config_object['bs_pi'],
                                                                      '/fapi/v1/order',
                                                                      stop_loss)
                                if 'msg' not in stop_loss_order:
                                    append_to_txt_file(stop_loss_order,
                                                       'positions_and_orders.txt')
                                    print(lg + get_current_date_time() +
                                          ' SL order modified. ' + n + '\n')
                                    value[0] = [stop_loss_order['orderId']]
                                    value[1][0] = 0
                                    with lock:
                                        positions.update({key: value})
                                    print(lg + get_current_date_time() + ' Modify SL Order...' + n + '\n')
                                else:
                                    print(r + get_current_date_time() + ' New error occurred: ' + str(
                                        stop_loss_order['msg']) + n + '\n')
                            else:
                                print(r + get_current_date_time() + ' New error occurred: ' + str(
                                    sl_cancel_response['msg']) + n + '\n')
                        else:
                            stop_loss = {
                                "symbol": key,
                                "side": 'SELL' if float(check_pos_filt[[pos[0]
                                                                        for pos in check_pos_filt].index(key)][
                                                            1]) > 0.0 else 'BUY',
                                "type": "STOP_MARKET",
                                "stopPrice": str(convert_to_precision(tick_size_number_of_decimals,
                                                                      check_pos_filt[[pos[0] for pos in check_pos_filt].index(key)][2])),
                                "closePosition": 'true',
                                "timeInForce": "GTE_GTC",
                                "workingType": 'MARK_PRICE'
                            }
                            stop_loss_order = send_signed_request(config_object, 'POST', config_object['bs_pi'],
                                                                  '/fapi/v1/order',
                                                                  stop_loss)
                            if 'msg' not in stop_loss_order:
                                append_to_txt_file(stop_loss_order,
                                                   'positions_and_orders.txt')
                                print(lg + get_current_date_time() +
                                      ' SL order modified. ' + n + '\n')
                                value[0] = [stop_loss_order['orderId']]
                                value[1][0] = 0
                                with lock:
                                    positions.update({key: value})
                                print(lg + get_current_date_time() + ' Modify SL Order...' + n + '\n')
                            else:
                                print(r + get_current_date_time() + ' New error occurred: ' + str(
                                    stop_loss_order['msg']) + n + '\n')
                else:
                    with lock:
                        positions.pop(key)
        with lock:
            json.dump(positions, open("positions.json", 'w'))
        time.sleep(300)


def check_existing_open_orders(config_object):
    global positions
    try:
        check_pos_list = send_signed_request(
            config_object, 'GET', config_object['bs_pi'], '/fapi/v2/positionRisk')
        if len(check_pos_list) > 0 and 'msg' not in check_pos_list:
            symbols = [check_pos['symbol'] for check_pos in check_pos_list if
                       abs(float(check_pos['positionAmt'])) > 0]
            open_orders_response = send_signed_request(
                config_object, 'GET', config_object['bs_pi'], '/fapi/v1/openOrders')
            if 'msg' not in open_orders_response:
                print(lg + ' Total current positions:' + str(len(symbols)) + n + '\n')
                for symbol in symbols:
                    check_live_open_orders(config_object, symbol, open_orders_response)
            else:
                print(r + get_current_date_time() + ' New error occurred: ' + str(
                    response['msg']) + n + '\n')
        else:
            print(lg + get_current_date_time() +
                  ' No existing open orders... \n')
        if not os.path.isfile("positions.json"):
            json.dump(positions, open("positions.json", 'w'))
        elif positions:
            json.dump(positions, open("positions.json", 'w'))
        else:
            positions = json.load("positions.json")
        sync_positions_thread = Thread(target=sync_positions, args=(config_object,))
        sync_positions_thread.start()
    except Exception as e:
        print(r + get_current_date_time() +
              ' New error occurred: ' + str(e) + n + '\n')


def place_position_and_orders(signal, config_object):
    if signal['EXCHANGES'] == 'Binance Futures':
        place_position_and_orders_futures(signal, config_object)
    else:
        print('Please use the Binance Futures Exchange')


# telegram functions
def start_websocket(config_object):
    api_id = config_object['rgb_id']
    api_hash = config_object['rgb_id_app']
    chat_id_scalping = [int(config_object['rgb_id_cht'])]

    client = TelegramClient('anon', api_id, api_hash)
    print(lg + get_current_date_time() +
          ' Telegram Connected! \n')

    @client.on(events.NewMessage(chats=chat_id_scalping))
    async def my_event_handler(event):
        try:
            if 'Entry Targets' in event.raw_text:
                print(lg + get_current_date_time() +
                      ' New Signal detected!' + n + '\n')
                decode_message_pattern_thread = Thread(
                    target=decode_message_pattern, args=(event.raw_text, config_object))
                decode_message_pattern_thread.start()
        except Exception as e:
            print(r + get_current_date_time() +
                  ' New error occurred: ' + str(e) + n + '\n')

    client.start()
    client.run_until_disconnected()


def decode_message_pattern(string, config_object):
    if search('Entry Targets', string):
        pair = string.split('⚡')[2].split('#')[1].replace('/', '').strip()
        exchanges = string.split('Exchanges:')[1].split(
            'Signal Type:')[0].strip()
        trade_type = string.split('Signal Type:')[1].split('Leverage')[
            0].split('(')[1].split(')')[0].strip()
        leverage = string.split('Leverage:')[1].split('Entry Targets:')[
            0].split('x)')[0].split('(')[1].strip()
        entry_point = string.split('Entry Targets:')[1].split(
            'Take-Profit Targets:')[0].strip()
        exit_points = check_exit_points(
            string.split('Take-Profit Targets:')[1], config_object['tp_no'])
        stop_loss = string.split('Stop Targets:')[1].strip()
        signal = {
            'SYMBOL': pair,
            'EXCHANGES': exchanges,
            'TRADE_TYPE': trade_type,
            'LEVERAGE': leverage,
            'ENTRY_POINT': entry_point,
            'EXIT_POINTS': exit_points,
            'STOP_LOSS': stop_loss
        }
        append_to_txt_file(signal, 'decoded_messages.txt')
        print(lg + get_current_date_time() +
              ' Signal successfully decoded!' + n + '\n')
        place_position_and_orders(signal, config_object)


# requests functions
def hashing(query_string, config_object):
    return hmac.new(config_object['bg_id_k'].encode('utf-8'), query_string.encode('utf-8'),
                    hashlib.sha256).hexdigest()


def dispatch_request(http_method, config_object):
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json;charset=utf-8',
        'X-MBX-APIKEY': config_object['bg_id']
    })
    return {
        'GET': session.get,
        'DELETE': session.delete,
        'PUT': session.put,
        'POST': session.post,
    }.get(http_method, 'GET')


def send_signed_request(config_object, http_method, base_api, url_path, payload={}):
    query_string = urlencode(payload)
    query_string = query_string.replace('%27', '%22')
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = 'timestamp={}'.format(get_timestamp())

    url = base_api + url_path + '?' + query_string + \
          '&signature=' + hashing(query_string, config_object)

    params = {'url': url, 'params': {}}
    response = dispatch_request(http_method, config_object)(**params)
    return response.json()


def send_public_request(config_object, base_api, url_path, payload={}):
    query_string = urlencode(payload, True)
    url = base_api + url_path
    if query_string:
        url = url + '?' + query_string
    response = dispatch_request('GET', config_object)(url=url)
    return response.json()


# main function 
if __name__ == '__main__':
    config_object = get_config_object()
    # check if connection is ok to exchange
    response = send_signed_request(
        config_object, 'GET', config_object['bs_pi'], '/fapi/v2/balance')
    if 'msg' in response:
        print(r + get_current_date_time() + ' New error occurred: ' + str(
            response['msg']) + n + '\n')
        sys.exit()
    else:
        USDT_balance = float(list(
            filter(lambda x: x['asset'] == 'USDT', response))[0]['balance'])
        print(lg + get_current_date_time() +
              ' Your USDT balance is: ' + str(USDT_balance) + n + '\n')
    check_existing_open_orders(config_object)
    start_websocket(config_object)
