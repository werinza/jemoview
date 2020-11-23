#!/usr/bin/python3
# -*- coding: utf-8 -*-
# aufruf: python3 jemoview.py fileName   (falls python V3 als python3 benannt ist)
# oder aufruf: python jemoview.py fileName   (falls python V3 als python benannt ist)
#
# jeti model viewer
global version
version = 'jemoview; version 2020-07-24'
#
# program extracts all relevant information from an input jeti transmitter file (.jsn)
# and prints it in a csv format using ';' as delimiters, suitable for excel/calc programs

import json
import os
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import IntVar

# --------------------------------     utility functions    --------------------------------------


def checkGlobal(out_buf_l, out_buf_w, fileout):
    # prüfen ob alle werte in out_buf identisch, dann sind die werte global
    glob = True
    for ii in range(len(out_buf_w)):
        if out_buf_w[0] != out_buf_w[ii]:
            glob = False
    if glob:
        fileout.write('\n' + 'Global')
        fileout.write(out_buf_w[0])
    else:
        for ii in range(len(out_buf_w)):
            fileout.write(out_buf_l[ii])
            fileout.write(out_buf_w[ii])


def getJaNein(aInt):
    if aInt == 0:
        return 'nein'
    if aInt == 1:
        return 'ja'


def getSwitch(aString):
    switches1 = [
        'nix', 'P1', 'P2', 'P4', 'P3', 'P5', 'P6', 'P7', 'P8', 'SA', 'SB', 'SC',
        'SD', 'SE', 'SF', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'P9', 'P10', 'SM',
        'SN', 'SO', 'SP'
    ]  # P3 and P4 müssen hier vertauscht sein (evtl Bug in Nummerierung von Sender)
    log = [
        'Log1', 'Log2', 'Log3', 'Log4', 'Log5', 'Log6', 'Log7', 'Log8', 'Log9',
        'Log10', 'Log11', 'Log12', 'Log13', 'Log14', 'Log15', 'Log16', 'Log17',
        'Log18', 'Log19', 'Log20', 'Log21', 'Log22', 'Log23', 'Log24', '?01',
        '?02', '?03', '?04', '?05', '?06', '?07', '?08'
    ]
    voi = [
        'V01', 'V02', 'V03', 'V04', 'V05', 'V06', 'V07', 'V08', 'V09', 'V10',
        'V11', 'V12', 'V13', 'V14', 'V15', '?24'
    ]
    mx = [
        'MX1', 'MX2', 'MX3', 'MX4', 'MX5', 'MX6', 'MX7', 'MX8', 'MX9', 'MX10',
        'MX11', 'MX12', 'MX13', 'MX14', 'MX15', 'MX16'
    ]
    gx = [
        'GX', 'GY', 'GZ', 'G/L', 'G/R', 'GXL', 'GXR', 'GHi', '?36', '?37',
        '?38', '?39', '?40', '?41', '?42', '?43'
    ]
    seq = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10']
    sonst = [
        'CH1', 'CH2', 'CH3', 'CH4', 'CH5', 'CH6', 'CH7', 'CH8', '?99', '?100',
        '?101', '?102', '?103', '?104', '?105', '?106', 'Tr1', 'Tr2', 'Tr3',
        'Tr4', 'Tr5', 'Tr6', '?113', '?114', '?115', '?116', 'C01', 'C02',
        'C03', 'C04', '?121', '?122', '?123', '?124', '?125', '?126', '?127',
        '?128', '?129', '?130'
    ]
    switches7 = log + voi + mx + gx + seq + sonst

    # prüfen ob aString genau 7 commas und 8 integers hat
    xx = aString.split(',')  # ist liste von strings
    if len(xx) != 8:
        return '-'
    for ii in xx:  # ii ist string
        if ii[0] in ('-', '+'):
            if not ii[1:].isdigit():
                return '-'
        elif not ii.isdigit():
            return '-'

    # switch number ist auf erster oder siebenter position
    xx = aString.split(',')[0]
    switchNo = int(xx)
    if switchNo == 0:
        yy = aString.split(',')[6]
        switchNo7 = int(yy)
        if switchNo7 >= 0:
            return switches7[switchNo7]
        else:
            return '-'
    else:
        return switches1[switchNo]


def printDict(aDict, fileout):
    for key in aDict:
        value = aDict[key]
        out = '\n' + str(key) + ';' + str(value) + ';'
        fileout.write(out)


def setDecimal(aInt, aValue):
    while aInt > 0:
        aValue = float(aValue) / 10
        aInt -= 1
    return aValue


# ----------------------------------  funktionen für jedes dict auf 1. ebene in alphabetischer sortierung     -----------------


def accel(modelData, fileout):
    fileout.write('\n\nBewegunssensor')
    printDict(modelData['Accel'], fileout)


def alarms(modelData, fileout):
    fileout.write('\n\nAlarme:')
    fileout.write(
        '\nNummer;Sensor;Wert;X <= / >;Schwellwert;Audio;AktivierungSw;Wiederholung;Sprachausgabe;aktiv'
    )
    rept = ['nein', 'ja', '3x']
    ind = 0
    for item in modelData['Alarms']['Data']:  # ist liste von dicts
        ind += 1
        activt = getJaNein(item['Active'])
        sw = getSwitch(item['Switch'])
        gt = '<='
        if item['Var-Greater'] == 1:
            gt = '>'
        audio = item['File']
        id = item['Sensor-ID']
        param = item['Sensor-Param']
        dec = item['Decimals']
        value = setDecimal(dec, item['Value'])
        if item['Repeat'] < len(rept):
            rep = rept[item['Repeat']]
        else:
            rep = '???AL'
        voi = getJaNein(item['Voice'])
        sensor = ''
        parm = ''
        if id in sensoren:
            sensor = sensoren[id][0]
            parm = sensoren[id][param]
        if ind == 1:
            sensor = 'Empfänger'
            parm = 'RX-Spannung'
        out = '\n' + str(
            ind) + ';' + sensor + ';' + parm + ';' + gt + ';' + str(
                value
            ) + ';' + audio + ';' + sw + ';' + rep + ';' + voi + ';' + activt
        fileout.write(out)


def audio(modelData, fileout):
    fileout.write('\n\nAudioplay:')
    printDict(modelData['Audio'], fileout)


def commands(modelData, fileout):
    fileout.write('\n\nCommands / Sprachkommandos:')
    printDict(modelData['Commands'], fileout)


def common(modelData, fileout):
    fileout.write('\n\nCommon Schalter:')
    #out = '\nTrim Schalter'
    #for item in modelData['Common']['Tr-Switches']: # ist liste
    #out = out + ';' + getSwitch(item[0])
    #fileout.write(out)
    switch = getSwitch(modelData['Common']['Throtle-Cut-Switch'])
    if switch != '-':
        out = '\nThrotle-Cut-Switch;' + switch
        fileout.write(out)
    switch = getSwitch(modelData['Common']['Throtle-Idle-Switch'])
    if switch != '-':
        out = '\nThrotle-Idle-Switch;' + switch
        fileout.write(out)
    switch = getSwitch(modelData['Common']['Autotrim-Switch'])
    if switch != '-':
        out = '\nAutotrim-Switch;' + switch
        fileout.write(out)
    switch = getSwitch(modelData['Common']['Trainer-Switch'])
    if switch != '-':
        out = '\nTrainer-Switch;' + switch
        fileout.write(out)
    switch = getSwitch(modelData['Common']['Logging-Switch'])
    if switch != '-':
        out = '\nLogging-Switch;' + switch
        fileout.write(out)
    switch = getSwitch(modelData['Common']['Marker-Switch'])
    if switch != '-':
        out = '\nMarker-Switch;' + switch
        fileout.write(out)
    switch = getSwitch(modelData['Common']['Telemetry-Voice-Switch'])
    if switch != '-':
        out = '\Telemetry-Voice-Switch;' + switch
        fileout.write(out)
    switch = getSwitch(modelData['Common']['Mnu-lft'])
    if switch != '-':
        out = '\nMenu-links;' + switch
        fileout.write(out)
    switch = getSwitch(modelData['Common']['Mnu-rgt'])
    if switch != '-':
        out = '\nMenu-rechts;' + switch
        fileout.write(out)
    switch = getSwitch(modelData['Common']['FM-Annonc'])
    if switch != '-':
        out = '\nFM-Annonc;' + switch
        fileout.write(out)
    switch = getSwitch(modelData['Common']['RC-Switch'][0])
    if switch != '-':
        out = '\nRC-Switch;' + switch
        fileout.write(out)


def controls(modelData, fileout):  # Sticks/Schalter setup (Voreinstellungen)
    fileout.write('\n\nSticks/Schalter Setup')
    switches1 = [
        'nix', 'P1', 'P2', 'P4', 'P3', 'P5', 'P6', 'P7', 'P8', 'SA', 'SB', 'SC',
        'SD', 'SE', 'SF', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO',
        'SP', '?P9', '?P10'
    ]  # P3 and P4 müssen hier vertauscht sein (evtl Bug in Nummerierung von Sender)
    empty = True
    for item in modelData['Controls']['Data']:  # ist liste von dicts
        ind = int(item['ID'])
        pos = int(item['Req-Pos'])
        if pos > 0:
            out = '\n' + switches1[ind] + ';hat Einschaltstellung'
            fileout.write(out)
            empty = False
    if empty:
        fileout.write('\nkeine Einschaltstellung')


def ctrlsound(modelData, fileout):
    if 'CtrlSound' not in modelData:  # sender version <3
        return
    fileout.write('\n\nTon Proportionalgeber')
    empty = True
    for item in modelData['CtrlSound']['Data']:  # ist liste von dicts
        sw = getSwitch(item[0])
        if sw != '-' and item[1] > 0:
            fileout.write('\n' + sw)
            empty = False
    if empty:
        fileout.write('\nkeine Töne')


def displayedtelemetry(modelData, fileout):
    fileout.write('\n\nTelemetrieanzeige für Standard;Flugphase; ' +
                  flugphasen[0])
    if len(modelData['Displayed-Telemetry']) == 0:
        fileout.write('\nkeine Anzeige')
        return
    fileout.write('\nNummer;Inhalt;Zoom')
    sysdisp = [
        '?dt00', 'Flugphasen', 'Antenne', '?dt03', 'RX-Spannung', 'Besitzer',
        '?dt06', 'Jetibox', 'Trim', 'Tx Akku', 'Flugzeit', '?dt11', '?dt12',
        'Bild', '?dt14'
    ]
    ind = 0
    for item in modelData['Displayed-Telemetry']:  # ist liste von dicts
        if int(item['Flight-Mode']) > 0:
            return
        ind += 1
        typ = int(item['Item-Type'])
        if typ == 0:  # leere Anzeige
            zoom = getJaNein(item['DblSize'])
            out = str(ind) + ';' + 'leer' + ';' + zoom
        elif typ == 1:  # Stoppuhren
            id = int(item['ID'])
            zoom = getJaNein(item['DblSize'])
            out = str(ind) + ';' + stoppuhren[id] + ';' + zoom
        elif typ == 2:  # Sensoren
            id = int(item['ID'])
            if id in sensoren:
                sensor = sensoren[id][0]
                parm = int(item['Param'])
                wert = sensoren[id][parm]
            else:
                sensor = 'Sensor'
                wert = 'fehlt'
            zoom = getJaNein(item['DblSize'])
            out = str(ind) + ';' + sensor + ' / ' + wert + ';' + zoom
        elif typ == 3:  # Systemfunktionen
            id = int(item['ID'])
            zoom = getJaNein(item['DblSize'])
            if id < len(sysdisp):
                txt = sysdisp[id]
            else:
                txt = '???DT'
            if id == 7:
                zoom = '-'
            out = str(ind) + ';' + txt + ';' + zoom
        elif typ == 4:  # Lua App
            id = int(item['ID'])
            if id in luaid:
                sensor = 'Lua App  ' + str(id)
            zoom = '-'
            out = str(ind) + ';' + sensor + ';' + zoom
        fileout.write('\n' + out)


def eventsounds(modelData, fileout):
    fileout.write('\n\nSprachausgabe/Ereignis:')
    if len(modelData['Event-Sounds']['Data']) == 0:
        fileout.write('\nkein Ereignis')
        return
    fileout.write('\nSchalter;Audio;Wiederholung')
    for item in modelData['Event-Sounds']['Data']:  # ist liste von dicts
        sw = getSwitch(item['Switch'])
        audio = item['File']
        rep = getJaNein(item['Repeat'])
        out = '\n' + sw + ';' + audio + ';' + rep
        fileout.write(out)


def flightmodes(modelData, fileout):
    fileout.write('\n\nFlugphasen: allgemeine Daten  ')
    fileout.write('\nNummer;Titel;Audio;Schalter;Verzögerung')
    ind = -1
    for item in modelData['Flight-Modes']['Data']:  # ist liste von dicts
        ind += 1
        id = int(item['ID'])
        label = item['Label']
        aud = item['Audio']
        delay = item['Delay']
        sw = getSwitch(item['Switch'])
        if sw == '-':
            sw = 'Standard'
        out = '\n' + str(id) + ';' + label + ';' + aud + ';' + sw + ';' + str(
            delay)
        fileout.write(out)
        flugphasen[ind] = label
    flugphasen[10] = ind  # anzahl flugphasen speichern

    # Vtail-Delta-Ailvator
    if qwhssafbd[8] != '':
        fileout.write('\n\nFlugphasen: ' + qwhssafbd[8])
        if qwhssafbd[8] == 'V-Leitwerksmischer':
            out_title = 'Flugphase;Höhe S1 / S2;Seite S1 / S2'
        else:
            out_title = 'Flugphase;Höhe S1 / S2;Quer S1 / S2'
        fileout.write('\n' + out_title)
        out_buf_l = []
        out_buf_w = []
        for item in modelData['Flight-Modes']['Data']:  # ist liste von dicts
            id = int(item['ID'])
            label = item['Label']
            w1 = str(item['VTail-Delta-Ailv'][0])
            w2 = str(item['VTail-Delta-Ailv'][1])
            w5 = str(item['VTail-Delta-Ailv'][4])
            w6 = str(item['VTail-Delta-Ailv'][5])
            outl = '\n' + label
            outw = ';' + w1 + ' / ' + w2 + ';' + w5 + ' / ' + w6
            out_buf_l.append(outl)
            out_buf_w.append(outw)
        checkGlobal(out_buf_l, out_buf_w, fileout)

    # QR Differenzierung
    if qwhssafbd[0] < 2:
        return
    fileout.write('\n\nQuerruderdifferenzierung')
    if qwhssafbd[0] == 2:
        fileout.write('\nFlugphase;Geber;Wirkung;Pos S1 / S2;Neg S1 / S2')
    if qwhssafbd[0] == 4:
        fileout.write(
            '\nFlugphase;Geber;Wirkung;Pos S1 / S2 / S3 / S4;Neg S1 / S2 / S3 / S4'
        )
    out_buf_l = []
    out_buf_w = []
    for item in modelData['Flight-Modes']['Data']:  # ist liste von dicts
        id = int(item['ID'])
        label = item['Label']
        qd_sw = getSwitch(item['ADiffSwitch'])
        wirk = str(item['ADiffVal'])
        qd_neg_s1 = str(item['ADiffPos'][0])
        qd_neg_s2 = str(item['ADiffPos'][1])
        qd_neg_s3 = str(item['ADiffPos'][2])
        qd_neg_s4 = str(item['ADiffPos'][3])
        qd_pos_s1 = str(item['ADiffNeg'][0])
        qd_pos_s2 = str(item['ADiffNeg'][1])
        qd_pos_s3 = str(item['ADiffNeg'][2])
        qd_pos_s4 = str(item['ADiffNeg'][3])
        outl = '\n' + label
        outw = ';' + qd_sw + ';' + wirk + ';' + qd_neg_s1 + ' / ' + qd_neg_s2 + ';' + qd_pos_s1 + ' / ' + qd_pos_s2
        if qwhssafbd[0] == 4:
            outw = ';' + qd_sw + ';' + wirk + ';' + qd_neg_s1 + ' / ' + qd_neg_s2 + ' / ' + qd_neg_s3 + ' / ' + qd_neg_s4 + ';' + qd_pos_s1 + ' / ' + qd_pos_s2 + ' / ' + qd_pos_s3 + ' / ' + qd_pos_s4
        out_buf_l.append(outl)
        out_buf_w.append(outw)
    checkGlobal(out_buf_l, out_buf_w, fileout)

    # Butterfly
    fileout.write('\n\nButterfly')
    out_title = '\nFlugphase;Geber;Offset'
    if qwhssafbd[0] == 2:
        out_title = out_title + ';' + 'Quer S1 / S2' + ';' + 'Dif Einst. S1 / S2'
    if qwhssafbd[0] == 4:
        out_title = out_title + ';' + 'Quer S1 / S2 / S3 / S4' + ';' + 'Dif Einst. S1 / S2 / S3 / S4'
    if qwhssafbd[1] == 2:
        out_title = out_title + ';' + 'Klappen S1 / S2'
    if qwhssafbd[1] == 4:
        out_title = out_title + ';' + 'Klappen S1 / S2 / S3 / S4'
    if qwhssafbd[2] == 1:
        out_title = out_title + ';' + 'Höhe S1'
    if qwhssafbd[2] == 2:
        out_title = out_title + ';' + 'Höhe S1 / S2'
    out_title = out_title + ';' + 'Höhe Kurve'
    fileout.write(out_title)
    # QR max 4 Werte, Dif max 4 Werte, Klappen max 4 Werte, HR max 2 Werte, Kurve ja falls nicht standard (Kurventyp und Punkte)
    out_buf_l = []
    out_buf_w = []
    for item in modelData['Flight-Modes']['Data']:  # ist liste von dicts
        id = int(item['ID'])
        label = item['Label']
        but_sw = getSwitch(item['BrakeSw'])
        offset = str(item['BkOffset'])
        but_qr_s1 = str(item['BrakeMix'][0])
        but_qr_s2 = str(item['BrakeMix'][1])
        but_qr_s3 = str(item['BrakeMix'][2])
        but_qr_s4 = str(item['BrakeMix'][3])
        but_wk_s1 = str(item['BrakeMix'][4])
        but_wk_s2 = str(item['BrakeMix'][5])
        but_wk_s3 = str(item['BrakeMix'][6])
        but_wk_s4 = str(item['BrakeMix'][7])
        but_hr_s1 = str(item['BrakeMix'][8])
        but_hr_s2 = str(item['BrakeMix'][9])
        but_qr_d1 = str(item['BrakeDiff'][0])
        but_qr_d2 = str(item['BrakeDiff'][1])
        but_qr_d3 = str(item['BrakeDiff'][2])
        but_qr_d4 = str(item['BrakeDiff'][3])
        curtyp = item['BrakeElevCurve']['Curve-Type']
        if curtyp < len(kurventyp):
            curve = kurventyp[curtyp]
        else:
            curve = '???KT'
        outl = '\n' + label
        outw = ';' + but_sw + ';' + offset
        if qwhssafbd[0] == 2:
            outw = outw + ';' + but_qr_s1 + ' / ' + but_qr_s2 + ';' + but_qr_d1 + ' / ' + but_qr_d2
        if qwhssafbd[0] == 4:
            outw = outw + ';' + but_qr_s1 + ' / ' + but_qr_s2 + ' / ' + but_qr_s3 + ' / ' + but_qr_s4 + ';' + but_qr_d1 + ' / ' + but_qr_d2 + ' / ' + but_qr_d3 + ' / ' + but_qr_d4
        if qwhssafbd[1] == 2:
            outw = outw + ';' + but_wk_s1 + ' / ' + but_wk_s2
        if qwhssafbd[1] == 4:
            outw = outw + ';' + but_wk_s1 + ' / ' + but_wk_s2 + ' / ' + but_wk_s3 + ' / ' + but_wk_s4
        if qwhssafbd[2] == 1:
            outw = outw + ';' + but_hr_s1
        if qwhssafbd[2] == 2:
            outw = outw + ';' + but_hr_s1 + ' / ' + but_hr_s1
        outw = outw + ';' + curve
        out_buf_l.append(outl)
        out_buf_w.append(outw)
    checkGlobal(out_buf_l, out_buf_w, fileout)


def functions(modelData, fileout):
    fileout.write('\n\nFunktionszuordnung:')
    fileout.write('\nNummer;Funktion;Geber;Trim extra;Trim max')
    for item in modelData['Functions']['Data']:  # ist liste von dicts
        id = item['ID']
        label = item['Label']
        control = getSwitch(item['Control'])
        trimcontrol = getSwitch(item['Trim-Control'])
        trimmax = item['Trim-Max']
        out = str(id) + ';' + label + ';' + control
        if trimcontrol != '-':
            out = out + ';' + trimcontrol + ';' + str(trimmax)
        fileout.write('\n' + out)
        funktionen[id] = label


def functionspecs(modelData, fileout):  # liste von dicts
    # Überschriften sammeln bei Flight-Mode 0
    out_title_trim = 'Flugphase'
    out_title_dr = 'Flugphase'
    out_title_expo = 'Flugphase'
    out_title_sw = 'Flugphase'
    out_title_curve = 'Flugphase'
    for item in modelData['Function-Specs']:  # ist liste von dicts
        flm = int(item['Flight-Mode'])
        if flm == 0:
            flmt = flugphasen[flm]
            fun = int(item['Function-Id'])
            funt = funktionen[fun]
            out_title_trim = out_title_trim + ';' + funt + ' Trim'
            out_title_dr = out_title_dr + ';' + funt + ' DR'
            out_title_expo = out_title_expo + ';' + funt + ' Expo'
            out_title_sw = out_title_sw + ';' + funt + ' Switch'
            out_title_curve = out_title_curve + ';' + funt + ' Kurve'
        else:
            break
    # daten sammeln
    out_buf_l = []
    out_trim_w = []
    out_trim = ''
    out_dr_w = []
    out_dr = ''
    out_expo_w = []
    out_expo = ''
    out_drsw_w = []
    out_drsw = ''
    out_curve_w = []
    out_curve = ''
    no_sw = True
    flmold = -1
    # speichern
    for item in modelData['Function-Specs']:  # ist liste von dicts
        flm = int(item['Flight-Mode'])
        flmt = flugphasen[flm]
        fun = int(item['Function-Id'])
        funt = funktionen[fun]
        trim1 = item['Ph-Trim'][0]
        trim2 = item['Ph-Trim'][1]
        trim3 = item['Ph-Trim'][2]
        trim4 = item['Ph-Trim'][3]
        drneg = item['DR-Neg'][0]
        drpos = item['DR-Pos'][0]
        sw = getSwitch(item['DR-Switch'])
        if sw != '-':
            no_sw = False
        exneg = item['Expo-Neg'][0]
        expos = item['Expo-Pos'][0]
        curtyp = item['Curve-Type']
        if curtyp < len(kurventyp):
            curve = kurventyp[curtyp]
        else:
            curve = '???KT'

        if flm == flmold:  # selbe flugphase fortsetzen / daten anhängen
            hit = False
            for txt in qwhssafbd_txt:
                if funt == txt:
                    hit = True
                    ii = qwhssafbd_txt.index(funt)
                    out_trim = out_trim + ';' + str(trim1)
                    if qwhssafbd[ii] == 2:
                        out_trim = out_trim + ' / ' + str(trim2)
                    if qwhssafbd[ii] == 3:
                        out_trim = out_trim + ' / ' + str(trim2) + ' / ' + str(
                            trim3)
                    if qwhssafbd[ii] == 4:
                        out_trim = out_trim + ' / ' + str(trim2) + ' / ' + str(
                            trim3) + ' / ' + str(trim4)
            if hit == False:
                out_trim = out_trim + ';' + str(trim1)
            out_dr = out_dr + ';' + str(drneg) + ' / ' + str(drpos)
            out_expo = out_expo + ';' + str(exneg) + ' / ' + str(expos)
            out_drsw = out_drsw + ';' + sw
            out_curve = out_curve + ';' + curve
        else:  # nächste flugphase mit erster funktion
            if flmold != -1:
                out_trim_w.append(out_trim)
                out_dr_w.append(out_dr)
                out_expo_w.append(out_expo)
                out_drsw_w.append(out_drsw)
                out_curve_w.append(out_curve)
            flmold = flm
            out_buf_l.append('\n' + flmt)
            hit = False
            for txt in qwhssafbd_txt:
                if funt == txt:
                    hit = True
                    ii = qwhssafbd_txt.index(funt)
                    out_trim = ';' + str(trim1)
                    if qwhssafbd[ii] == 2:
                        out_trim = out_trim + ' / ' + str(trim2)
                    if qwhssafbd[ii] == 3:
                        out_trim = out_trim + ' / ' + str(trim2) + ' / ' + str(
                            trim3)
                    if qwhssafbd[ii] == 4:
                        out_trim = out_trim + ' / ' + str(trim2) + ' / ' + str(
                            trim3) + ' / ' + str(trim4)
            if hit == False:
                out_trim = ';' + str(trim1)
            out_dr = ';' + str(drneg) + ' / ' + str(drpos)
            out_expo = ';' + str(exneg) + ' / ' + str(expos)
            out_drsw = ';' + sw
            out_curve = ';' + curve
    out_trim_w.append(out_trim)
    out_dr_w.append(out_dr)
    out_expo_w.append(out_expo)
    out_drsw_w.append(out_drsw)
    out_curve_w.append(out_curve)

    # daten ausgeben
    fileout.write('\n\nFlugphasentrimmung')
    fileout.write('\n' + out_title_trim)
    checkGlobal(out_buf_l, out_trim_w, fileout)
    fileout.write(
        '\n\nDualRate                  --- ;   Werte gelten nur;   falls kein;   DR-Schalter;   zugeordnet'
    )
    fileout.write('\n' + out_title_dr)
    checkGlobal(out_buf_l, out_dr_w, fileout)
    fileout.write('\n\nDualRate Schalter')
    if no_sw:
        fileout.write('\nkeine Schalter')
    else:
        fileout.write('\n' + out_title_sw)
        checkGlobal(out_buf_l, out_drsw_w, fileout)
    fileout.write('\n\nExpo')
    fileout.write('\n' + out_title_expo)
    checkGlobal(out_buf_l, out_expo_w, fileout)
    fileout.write('\n\nFunktionskurven')
    fileout.write('\n' + out_title_curve)
    checkGlobal(out_buf_l, out_curve_w, fileout)


def globalstr(modelData, fileout):
    fileout.write('\n\nGlobale Einstellungen:')
    # sender aus www.jetimodel.com/en/DC-DS-24-Lua-API-1/Lua-Programming-API-for-DC-DS-24/
    sender = ['DC-16', 'DS-16', 'DS-14', 'DC-14', 'DC-24', 'DS-24', 'DS-12']
    typ = ['Flugzeug', 'Heli', 'Truck/Boat', 'X-Copter']
    for item in modelData['Global']:
        itemt = str(item)
        if item == 'Type':
            continue
        if item == 'Version':  # sender version <5
            value = int(modelData['Global'][item])
            if value == 1:  #
                continue
            if value > 673 and value - 674 < len(sender):
                out = '\nSender Typ' + ';' + sender[value - 674]
            else:
                out = '\nSender Typ' + ';' + '???TX'
            fileout.write(out)
            continue
        if item == 'Name' or item == 'Desc':
            txt = modelData['Global'][item]
            out = '\n' + item + ';' + txt
            fileout.write(out)
            continue
        if item == 'Receiver-ID1' or item == 'Receiver-ID2':
            itemt = item.replace('Receiver', 'Empfänger')
            value = int(modelData['Global'][item])
            if value > 0:
                z2 = int(value / 65536)
                z1 = value - z2 * 65536
                out = itemt + ';' + str(z1) + ':' + str(z2)
            else:
                out = itemt + ';' + '-'
            fileout.write('\n' + out)
            continue
        if item == 'Rx-ID900':
            value = int(modelData['Global'][item])
            if value > 0:
                z2 = int(value / 65536)
                z1 = value - z2 * 65536
                out = itemt + ';' + str(z1) + ':' + str(z2)
            else:
                out = itemt + ';' + '-'
            fileout.write('\n' + out)
            continue
        if item == 'TxVers':
            itemt = 'Sender Version'
        if item == 'Model-Type':
            ind = int(modelData['Global'][item]) - 1
            if ind < len(typ):
                out = 'Modelltyp' + ';' + typ[ind]
            else:
                out = 'Modelltyp' + ';' + '???MT'
        else:
            out = itemt + ';' + str(modelData['Global'][item])
        fileout.write('\n' + out)


def iqsdata(modelData, fileout):
    fileout.write('\nIQSData:')
    printDict(modelData['IQSData'], fileout)


def logswitch(modelData, fileout):
    fileout.write('\n\nLogische Schalter:')
    logtyp = ['...', 'And', 'Or', 'Multi']
    # zuerst den letzten logswitch suchen der ungleich default
    last = len(modelData['LogSwitch']['Data'])
    empty = True
    for ii in range(last - 1, -1, -1):
        item = modelData['LogSwitch']['Data'][ii]
        enabled = item['Enabled']
        label = item['Label']
        sw1 = getSwitch(item['Switch1'])
        if item['Log-Type'] < len(logtyp):
            zutxt = logtyp[item['Log-Type']]
        else:
            zutxt = '???L'
        sw2 = getSwitch(item['Switch2'])
        if enabled != 0 or label != '' or sw1 != '-' or zutxt != '...' or sw2 != '-':
            empty = False
            last = ii
            break
    if empty:
        fileout.write('\nkeine Schalter')
        return
    fileout.write('\nNummer;Titel;Geber1;Zustand;Geber2;aktiv')
    for item in modelData['LogSwitch']['Data']:  # ist liste von dicts
        ind = int(item['Index'])
        if ind > last:
            return
        enabled = getJaNein(item['Enabled'])
        label = item['Label']
        sw1 = getSwitch(item['Switch1'])
        if item['Log-Type'] < len(logtyp):
            zutxt = logtyp[item['Log-Type']]
        else:
            zutxt = '???L'
        zutxt = logtyp[item['Log-Type']]
        sw2 = getSwitch(item['Switch2'])
        out = '\nLog' + str(
            ind + 1
        ) + ';' + label + ';' + sw1 + ';' + zutxt + ';' + sw2 + ';' + enabled
        fileout.write(out)


def lua(modelData, fileout):
    fileout.write('\n\nLua:')
    if 'Lua' not in modelData:
        fileout.write('\nkeine Lua Daten')
        return
    anz = len(modelData['Lua'])
    if anz > 0:
        ind = 1
        for item in modelData['Lua']:  # ist liste von dicts
            luaid[ind] = item['appID']
            out = '\n' + str(ind) + ';Lua App ID;' + str(luaid[ind])
            # wir nehmen an dass luadata immer gruppen von 3 elementen sind, zuerst string gefolgt von 2 weiteren daten
            # angezeigt werden hier nur solche gruppen, die einnen schalter oder einen sensor enthalten
            luadata = item['data']
            counter = 0
            out3 = ''
            for dat in luadata:
                if len(out3) > 0:
                    out = out + ';' + out2 + ';' + out3
                out3 = ''
                if counter % 3 == 0:
                    out2 = str(dat)
                else:
                    sw = getSwitch(str(dat))
                    if sw != '-':
                        if len(out3) == 0:
                            out3 = sw
                        else:
                            out3 = out3 + ';' + sw
                    if type(dat) == int:
                        if dat in sensoren:
                            if len(out3) == 0:
                                out3 = sensoren[dat][0]
                            else:
                                out3 = out3 + ';' + sensoren[dat][0]
                counter += 1
            if len(out3) > 0:
                out = out + ';' + out2 + ';' + out3
            fileout.write(out)
            ind += 1
    else:
        fileout.write('\nkeine Lua App')


def luactrl(modelData, fileout):
    fileout.write('\n\nLua-Ctrl:')
    printDict(modelData['Lua-Ctrl'], fileout)


def mixesmain(modelData, fileout):
    fileout.write('\n\nFreie Mischer: Übersicht')
    if len(modelData['Mixes-Main']['Data']) == 0:
        fileout.write('\nkeine Mischer')
        return
    fileout.write('\nvon;auf;Wirkung;asym Gas Mischer')
    anz_mix = 0
    for item in modelData['Mixes-Main']['Data']:  # ist liste von listen
        anz_mix += 1
        von = funktionen[item[0]]
        auf = funktionen[item[1]]
        wirk = 'Flugphasen abhängig'
        if item[2] == 1:
            wirk = 'Global'
        asym = 'nein'
        if von == 'Drossel':
            asym = getJaNein(item[3])
        out = '\n' + von + ';' + auf + ';' + wirk + ';' + asym
        fileout.write(out)

    fileout.write('\n\nFreie Mischer: Flugphasen')
    fileout.write(
        '\nMischer;Flugphase;Wert;Switch;Kurve;MixAusgabe + ;MixAusgabe - ;nur vorwärts;MasterLink;SlaveLink;Trim;SlaveDualRate'
    )
    for ii in range(anz_mix):
        for jj in range(flugphasen[10] + 1):
            item = modelData['Mixes-Main']['Data'][ii]
            out = funktionen[item[0]] + ' auf ' + funktionen[item[1]]
            kk = jj * anz_mix + ii
            dic = modelData['Mixes-Values'][kk]
            flugphase = flugphasen[int(dic['Flight-Mode'])]
            wert = dic['Intensity']
            sw = getSwitch(dic['Switch'])
            mp1 = str(dic['S-Output'][0])
            mp2 = str(dic['S-Output'][1])
            mp3 = str(dic['S-Output'][2])
            mp4 = str(dic['S-Output'][3])
            if 'S-OutputN' in dic:
                mn1 = str(dic['S-OutputN'][0])
                mn2 = str(dic['S-OutputN'][1])
                mn3 = str(dic['S-OutputN'][2])
                mn4 = str(dic['S-OutputN'][3])
            else:  # sender version <3
                mn1 = 0
                mn2 = 0
                mn3 = 0
                mn4 = 0
            mixpo = ''
            mixno = ''
            for txt in qwhssafbd_txt:
                if funktionen[item[1]] == txt:
                    ll = qwhssafbd_txt.index(txt)
                    if qwhssafbd[ll] == 1:
                        mixpo = '-'
                        mixno = '-'
                    if qwhssafbd[ll] == 2:
                        mixpo = mp1 + ' / ' + mp2
                        mixno = mn1 + ' / ' + mn2
                    if qwhssafbd[ll] == 3:
                        mixpo = mp1 + ' / ' + mp2 + ' / ' + mp3
                        mixno = mn1 + ' / ' + mn2 + ' / ' + mn3
                    if qwhssafbd[ll] == 4:
                        mixpo = mp1 + ' / ' + mp2 + ' / ' + mp3 + ' / ' + mp4
                        mixno = mn1 + ' / ' + mn2 + ' / ' + mn3 + ' / ' + mn4
            vorw = getJaNein(dic['Direction'])
            ml = getJaNein(dic['M-Link'])
            sl = getJaNein(dic['S-Link'])
            trim = getJaNein(dic['M-Trim'])
            sdr = getJaNein(dic['S-DR'])
            curtyp = dic['Curve-Type']
            if curtyp < len(kurventyp):
                curve = kurventyp[curtyp]
            else:
                curve = '???KT'
            if item[2] == 1:  # ist global
                flugphase = 'Global'
            out = out + ';' + flugphase + ';' + str(
                wert
            ) + ';' + sw + ';' + curve + ';' + mixpo + ';' + mixno + ';' + vorw + ';' + ml + ';' + sl + ';' + trim + ';' + sdr
            fileout.write('\n' + out)
            if item[2] == 1:  # ist global
                break


def mixesvalues(modelData, fileout):
    fileout.write('Mixes-Values:')
    for item in modelData['Mixes-Values']:  # ist liste von dicts
        fileout.write(item)


def sequence(modelData, fileout):
    fileout.write('\n\nSequenzer:')
    out_title = '\nNummer;Titel;Switch;beeinflusst Servo;Typ;zyklisch;immer beenden'
    empty = True
    done = False
    for item in modelData['Sequence']:  # ist liste von dicts
        leer = True
        id = item['ID']
        sw = getSwitch(item['Switch'])
        label = item['Label']
        servo = item['Override']
        serout = servolist[servo]
        if serout == 'nix':
            serout = '-'
        if sw != '-' or label != '' or servo > 0:
            leer = False
        asym = 'symmetrisch'
        if getJaNein(item['Asymm']) == 'ja':
            asym = 'asymmetrisch'
        cyc = getJaNein(item['Cycle'])
        fin = getJaNein(item['Finish'])
        out = '\nQ' + str(
            id
        ) + ';' + label + ';' + sw + ';' + serout + ';' + asym + ';' + cyc + ';' + fin
        if not leer:
            if not done:
                fileout.write(out_title)
                done = True
            fileout.write(out)
            empty = False
    if empty:
        fileout.write('\nkeine Sequenzer')


def servos(modelData, fileout):
    fileout.write('\n\nServozuordnung:')
    fileout.write(
        '\nSteckplatz;Servo;Mittenverstellung;Max;Min;Wegumkehr;Verzögerung')
    servoNames = [
        'Querruder1', 'Querruder2', 'Querruder3', 'Querruder4', 'Klappe1',
        'Klappe2', 'Klappe3', 'Klappe4', 'Seite1', 'Seite2', 'Höhe1', 'Höhe2',
        '?269', '?270', 'Drossel1', 'Drossel2', 'Drossel3', 'Drossel4',
        'Fahrwerk1', 'Fahrwerk2', 'Fahrwerk3', 'Fahrwerk4', 'Störkl.1',
        'Störkl.2', 'Roll', 'Nick', 'Pitch', '?284', 'Heck', '?286',
        'Gyroempf.', '?288', '?289', '?290', '?291', '?292', '?293', '?294',
        '?295', '?296', '?297', '?298', '?299', '?300', '?301', '?302', '?303',
        '?304', 'Gyroempf.2', 'Gyroempf.3', 'Gimbal R', 'Gimbal P', '?309',
        'Mode', '?311', '?312', '?313', '?314', '?315', '?316', '?317', '?318',
        '?319', '?320'
    ]
    # ab 288 werden beliebige selbst erzeugte Namen von Funktionen verwendet und in servoSonst gespeichert
    # aber wieder fest für X-Copter (unklar ab wo - 304 angenommen)
    servoSonst = 16 * ['nix']  # non-Standard names
    # code ist evtl fehlerhaft wenn Annahmen falsch
    for item in modelData['Servos']['Data']:  # ist liste von dicts
        servo = int(item['Servo-Code'])
        if servo >= 288 and servo < 300:
            servoSonst[servo - 288] = servo
    # non-Standard Funktionen auf sonstige Servos zuordnen,
    # früheste non-Standard Funktion ab 14 entspricht Servo 288 (ist auf servoSonst[0]), 15 auf 289 usw
    # höchste mit 29 angenommen (16 Stück)
    ind = 13
    for ii in range(16):
        ind += 1
        if str(servoSonst[ii]) != 'nix':
            if funktionen[ind] != 'nix':
                servoSonst[ii] = funktionen[ind]
    # jetzt alle Servos detaillieren
    for item in modelData['Servos']['Data']:  # ist liste von dicts
        ind = int(item['Index']) + 1
        servo = int(item['Servo-Code'])
        middle = item['Middle']
        maxp = item['Max-Positive']
        maxn = item['Max-Negative']
        reverse = ';' + getJaNein(item['Servo-Reverse'])
        delayp = int(item['Delay-Positive'])
        delayn = int(item['Delay-Negative'])
        delayed = ';nein'
        if delayp > 0 or delayn > 0:
            delayed = ';ja'
        # namen zuordnen
        if servo > 256:
            if servo <= 287:  # Standard Servos
                name = servoNames[servo - 257]
            elif servo >= 300:  # Standard Servos
                if servo - 257 < len(servoNames):
                    name = servoNames[servo - 257]
                else:
                    name = '???SN'
            else:  # sonstige Servos
                name = str(servoSonst[servo - 288])
            out = '\n' + str(ind) + ';' + name + ';' + str(middle) + ';' + str(
                maxp) + ';' + str(maxn) + reverse + delayed
            fileout.write(out)
            servolist[ind] = name


def snaprolls(modelData, fileout):
    if qwhssafbd[8] == 'V-Leitwerksmischer' or qwhssafbd[
            8] == 'Delta/Elevon Mischer':
        return  # nicht bei v-lw oder nurflügel
    fileout.write('\n\nSnap Rolls:')
    out_title = '\nFlugphase;Mode;Master Switch;Sw Höhe/rechts;Sw Tiefe/rechts;Sw Höhe/links;Sw Tiefe/links'
    empty = True
    done = False
    for item in modelData['SnapRolls']:  # ist liste von dicts
        leer = True
        out = ''
        flm = int(item['Flight-Mode'])
        flmt = flugphasen[flm]
        mode = item['Mode']
        if mode == 0:
            modet = 'Master'
            sw = getSwitch(item['Master-Sw'])
            if sw != '-':
                leer = False
        else:
            modet = 'Single'
            sw = '-'
            leer = False
        out = flmt + ';' + str(modet) + ';' + sw
        for ii in range(4):
            swx = getSwitch(item['Switch'][ii])
            out = out + ';' + swx
        if not leer:
            if not done:
                fileout.write(out_title)
                done = True
            fileout.write('\n' + out)
            empty = False
    if empty:
        fileout.write('\nkeine Snap Rolls')


def telctrl(modelData, fileout):
    if 'Tel-Ctrl' not in modelData:  # sender version <3
        return
    fileout.write('\n\nTelemetriegeber:')
    # zuerst den letzten telctrl suchen der ungleich default
    last = len(modelData['Tel-Ctrl']['Data'])
    empty = True
    for ii in range(last - 1, -1, -1):
        item = modelData['Tel-Ctrl']['Data'][ii]
        enabled = item['Enabled']
        label = item['Label']
        id = item['Sensor-ID']
        sw = getSwitch(item['Switch'])
        prop = item['Prop']
        if enabled != 0 or label != '' or id != 0 or sw != '-' or prop != 0:
            empty = False
            last = ii
            break
    if empty:
        fileout.write('\nkeine Telemetriegeber')
        return
    fileout.write(
        '\nNummer;Titel;Sensor;Wert;Gebertyp;X < = > / Weite1;Schwellw. / Weite2;Toleranz / Weite3;Dauer / Glättung;Standardw %;Switch;aktiv'
    )
    comp = ['<', '>', '=']
    for item in modelData['Tel-Ctrl']['Data']:  # ist liste von dicts
        ind = int(item['Index'])
        if ind > last:
            return
        enabled = getJaNein(int(item['Enabled']))
        label = item['Label']
        id = item['Sensor-ID']
        if id in sensoren:
            sensor = sensoren[id][0]
            wert = sensoren[id][item['Param']]
            out = 'MX' + str(ind + 1) + ';' + label + ';' + sensor + ';' + wert
        else:
            out = 'MX' + str(ind + 1) + ';' + label + ';' + '-' + ';' + '-'
        if item['Prop'] == 0:
            out = out + ';Switch'
            dat = item['Bin-Data']  # ist list
            dec = item['Decimals']
            w1 = comp[dat[0]]
            w2 = setDecimal(dec, dat[2])
            w3 = setDecimal(dec, dat[3])
            w4 = setDecimal(1, dat[1])
            stand = item['Default']
            sw = getSwitch(item['Switch'])
            out = out + ';' + str(w1) + ';' + str(w2) + ';' + str(
                w3) + ';' + str(w4) + ';' + str(stand) + ';' + sw
        else:
            out = out + ';Proportional'
            dat = item['Prop-Data']  # ist list
            dec = item['Decimals']
            w1 = setDecimal(dec, dat[0])
            w2 = setDecimal(dec, dat[1])
            w3 = setDecimal(dec, dat[2])
            w4 = setDecimal(0, dat[3])
            stand = item['Default']
            sw = getSwitch(item['Switch'])
            out = out + ';' + str(w1) + ';' + str(w2) + ';' + str(
                w3) + ';' + str(w4) + ';' + str(stand) + ';' + sw
        out = out + ';' + enabled
        fileout.write('\n' + out)


def telemdetect(modelData, fileout):
    fileout.write('\n\nSensoren und Einstellungen:')
    out_title = '\nSensor;Wert;Wiederholung;Trigger;Wichtigkeit'
    fileout.write(out_title)
    prio = ['niedrig', 'mittel', 'hoch']
    # zuerst die festen U-Rx, A1 und A2 aus Voice extrahieren
    voc = ['U-Rx', 'A1', 'A2']
    voct = ['Rx-Spannung', 'Antenne 1', 'Antenne 2']
    for ii in range(3):
        rep = getJaNein(modelData['Voice'][voc[ii]][0])
        trig = getJaNein(modelData['Voice'][voc[ii]][1])
        priot = prio[modelData['Voice'][voc[ii]][2]]
        out = '\nEmpfänger;' + voct[ii] + ';' + rep + ';' + trig + ';' + priot
        fileout.write(out)
    if len(modelData['Telem-Detect']['Data']) == 0:
        return
    id = ''
    geraet = 65 * ['nix']
    for item in modelData['Telem-Detect']['Data']:  # ist liste von dicts
        ind = int(item['Param'])
        if ind == 0:  # neues gerät / sensor
            if id != '':
                sensoren[id] = geraet  # parameter voriges gerät speichern
            id = item['ID']
            geraet = 65 * ['nix']
        geraet[ind] = item['Label']
        rep = getJaNein(item['Rep'])
        trig = getJaNein(item['Trig'])
        priot = prio[item['Prio']]
        out = '\n' + str(geraet[0]) + ';' + str(
            geraet[ind]) + ';' + rep + ';' + trig + ';' + priot
        fileout.write(out)
    sensoren[id] = geraet  # parameter letztes gerät speichern


def telemvoice(modelData, fileout):
    fileout.write('\n\nEinzelsprachansagen:')
    if 'Telem-Voice' not in modelData:  # existiert in V3 nicht
        fileout.write('\nkeine Sprachansage')
        return
    if len(modelData['Telem-Voice']['Data']) == 0:
        fileout.write('\nkeine Sprachansagen')
        return
    fileout.write('\nSensor;Wert;Schalter')
    for item in modelData['Telem-Voice']['Data']:  # ist liste von dicts
        key = item['ID']
        parm = int(item['Param'])
        sw = getSwitch(item['Sw'])
        if key in sensoren:
            out = sensoren[key][0] + ';' + sensoren[key][parm] + ';' + sw
        else:
            out = 'Sensor fehlt:;' + str(key) + ';' + sw
        fileout.write('\n' + out)


def timers(modelData, fileout):
    fileout.write('\n\nStoppuhren:')
    if len(modelData['Timers']['Data']) == 0:
        fileout.write('\nkeine Stoppuhren')
        return
    fileout.write('\nName;Schalter')
    for item in modelData['Timers']['Data']:  # ist liste von dicts
        id = int(item['ID'])
        sw = getSwitch(item['Switch'])
        out = '\n' + item['Label'] + ';' + str(sw)
        fileout.write(out)
        stoppuhren[id] = item['Label']


def typespecific(modelData, fileout):
    fileout.write('\n\nGrundeinstellungen:')
    if modelData['Type-Specific']['Model-Type'] != 'Aero':
        printDict(modelData['Type-Specific'], fileout)
        return
    wing = ['1QR', '2QR', '2QR+1WK', '2QR+2WK', '4QR+2WK', '2QR+4WK', '4QR+4WK']
    wing_qr = [1, 2, 2, 2, 4, 2, 4]
    wing_wk = [0, 0, 1, 2, 2, 4, 4]
    tail = [
        'Kreuz od T-LW 1HR 1SR', 'V-LW 2 Servos', 'Ailvator 2HR 1SR',
        '2HR / 2SR', 'kein LW (Delta/Elevon)', 'kein LW'
    ]
    tail_hr = [1, 2, 2, 2, 2, 0]
    tail_sr = [1, 2, 1, 2, 1, 0]
    for item in modelData['Type-Specific']:
        out = ''
        if item == 'Type' or item == 'Model-Type':
            continue
        if item == 'Wing-Type':
            ind = int(modelData['Type-Specific'][item])
            if ind < len(wing):
                out = 'Tragfläche' + ';' + wing[ind]
                qwhssafbd[0] = wing_qr[ind]
                qwhssafbd[1] = wing_wk[ind]
            else:
                out = 'Tragfläche' + ';' + '???TS'
                qwhssafbd[0] = 0
                qwhssafbd[1] = 0
        if item == 'Tail-Type':
            ind = int(modelData['Type-Specific'][item])
            if ind < len(tail):
                out = 'Leitwerk' + ';' + tail[ind]
                qwhssafbd[2] = tail_hr[ind]
                qwhssafbd[3] = tail_sr[ind]
            else:
                out = 'Leitwerk' + ';' + '???TT'
                qwhssafbd[2] = 0
                qwhssafbd[3] = 0
            if ind == 1:
                qwhssafbd[8] = 'V-Leitwerksmischer'
            if ind == 2:
                qwhssafbd[8] = 'Ailevator'
                if qwhssafbd[0] >= 2:
                    qwhssafbd[7] = 1
            if ind == 4:
                qwhssafbd[8] = 'Delta/Elevon Mischer'
                qwhssafbd[7] = 1
        if item == 'Motor-Count':
            anz = int(modelData['Type-Specific'][item])
            out = 'Antriebe' + ';' + str(anz)
            qwhssafbd[5] = anz
        if item == 'Gear-Servos':
            anz = int(modelData['Type-Specific'][item])
            out = 'Fahrwerke' + ';' + str(anz)
            qwhssafbd[6] = anz
        if item == 'Airbrake-Servos':
            anz = int(modelData['Type-Specific'][item])
            out = 'Störklappen' + ';' + str(anz)
            qwhssafbd[4] = anz
        for ii in range(3):
            wert = 'nein'
            txt = 'Gyro' + str(ii + 1)
            if item == txt:
                if int(modelData['Type-Specific'][item]) == 1:
                    wert = 'ja'
                out = txt + ';' + wert
        if len(out) > 0:
            fileout.write('\n' + out)


def usermenu(modelData, fileout):
    fileout.write('\n\nUser-Menu:')
    printDict(modelData['User-Menu'], fileout)


def vario(modelData, fileout):
    fileout.write('\n\nVario:')
    if 'Setting' not in modelData['Vario']:
        fileout.write(
            '\nDaten in altem Format; Sender updaten auf Version 4.28 oder höher'
        )
        return
    empty = True
    modes = ['Aus', 'Alarm JB Profi', 'Wert EX', 'Lua']
    mode = modelData['Vario']['Mode']
    if mode < len(modes):
        modet = modes[mode]
    else:
        modet = '???VM'
    sw = getSwitch(modelData['Vario']['Switch'])
    setting = modelData['Vario']['Setting']  # ist liste von dicts
    for ii in range(len(modelData['Vario']['Setting'])):
        id = modelData['Vario']['Setting'][ii]['Sensor-ID']
        param = int(modelData['Vario']['Setting'][ii]['Sensor-Par'])
        dec = int(modelData['Vario']['Setting'][ii]['Decimals'])
        deadzpos = str(
            setDecimal(dec, int(modelData['Vario']['Setting'][ii]['DeadZPos'])))
        deadzneg = str(
            setDecimal(dec, int(modelData['Vario']['Setting'][ii]['DeadZNeg'])))
        minw = str(
            setDecimal(dec, int(modelData['Vario']['Setting'][ii]['Min'])))
        center = str(
            setDecimal(dec, int(modelData['Vario']['Setting'][ii]['Center'])))
        maxw = str(
            setDecimal(dec, int(modelData['Vario']['Setting'][ii]['Max'])))
        enabled = getJaNein(modelData['Vario']['Setting'][ii]['En'])
        #value = setDecimal(dec, item['Value'])
        if id in sensoren:
            sensor = sensoren[id][0]
            parm = sensoren[id][param]
            if empty:
                fileout.write('\nMode;' + modet)
                fileout.write('\nSchalter;' + sw)
                fileout.write(
                    '\nSensor;Wert;Totzone -;Totzone +;Weite -;Center;Weite +;aktiv'
                )
                empty = False
            out = '\n' + sensor + ';' + parm + ';' + deadzneg + ';' + deadzpos + ';' + minw + ';' + center + ';' + maxw + ';' + enabled
            fileout.write(out)
    if empty:
        fileout.write('\nkein Vario')


def voice(modelData, fileout):
    fileout.write('\n\nSprachausgabe:')
    out = ''
    sw = getSwitch(modelData['Voice']['TimerSw'])
    if sw != '-':
        timer = modelData['Voice']['Timer-ID']
        out = '\nTimer;' + stoppuhren[timer] + ';Switch;' + sw
        fileout.write(out)
    sw = getSwitch(modelData['Voice']['RepeatSw'])
    if sw != '-':
        time = modelData['Voice']['Timeout']
        out = '\nWiederh. nach;' + str(time) + 'sec;Switch;' + sw
        fileout.write(out)
    sw = getSwitch(modelData['Voice']['TrigSw'])
    if sw != '-':
        out = '\nTrigger;;Schalter;' + sw
        fileout.write(out)
    if out == '':
        fileout.write('\nkeine Sprachausgabe')


def voicerec(modelData, fileout):
    fileout.write('\n\nVoiceRec:')
    printDict(modelData['VoiceRec'], fileout)


#--------------------------------    funktion zur auswertung der model datei    --------------------------------------
def extract(modelData, fileout):

    global funktionen
    global flugphasen
    global kurventyp
    global luaid
    global sensoren
    global servolist
    global stoppuhren
    global qwhssafbd  # anzahl_servos: qr wk hr sr stör antriebe fahrwerke butterfly(1=braucht butterfly) delta/v-lw
    global qwhssafbd_txt

    # anfangswerte setzen für globals, bei jedem model erneut
    funktionen = 51 * ['nix']
    flugphasen = 11 * ['nix']
    kurventyp = [
        'Standard', 'konstant', 'x>0', 'x<0', '|x|', '+positiv', '-negativ',
        'symmetrisch', '3-Punkt', '5-Punkt', '7-Punkt', '9-Punkt', 'Gyro'
    ]
    luaid = 31 * [0]
    sensoren = {}
    servolist = 25 * ['nix']
    stoppuhren = 11 * ['nix']
    qwhssafbd = [0, 0, 0, 0, 0, 0, 0, 0, '']
    qwhssafbd_txt = [
        'Quer', 'Klappen', 'Höhe', 'Seite', 'Störkl.', 'Drossel', 'Fahrwerk',
        '', ''
    ]

    # alle dicts auswerten
    globalstr(modelData, fileout)
    typespecific(modelData, fileout)  #schreibt qwhssafbd[]
    common(modelData, fileout)
    controls(modelData, fileout)
    ctrlsound(modelData, fileout)
    functions(modelData, fileout)  #schreibt funktionen[]
    servos(modelData, fileout)  #schreibt servolist[] und liest funktionen[]
    flightmodes(modelData, fileout)  #schreibt flugphasen[] und liest qwhssafbd[]
    functionspecs(modelData, fileout)  #liest funktionen[], flugphasen[], qwhssafbd[]
    mixesmain(modelData, fileout)  #liest funktionen[], flugphasen[], qwhssafbd[]
    #mixesvalues(modelData, fileout)        #in mixesmain() verarbeitet
    snaprolls(modelData, fileout)  #liest flugphasen[], qwhssafbd[]
    sequence(modelData, fileout)  #liest servolist[]
    timers(modelData, fileout)  #schreibt stoppuhren[]
    logswitch(modelData, fileout)
    voice(modelData, fileout)  #liest stoppuhren[]
    telemdetect(modelData, fileout)  #schreibt sensoren[]
    telemvoice(modelData, fileout)  #liest sensoren[]
    telctrl(modelData, fileout)  #liest sensoren[]
    lua(modelData, fileout)  #schreibt luaid[] und liest sensoren[]
    displayedtelemetry(modelData, fileout)  # liest luaid[], sensoren[], stoppuhren[]
    eventsounds(modelData, fileout)
    vario(modelData, fileout)  #liest sensoren[]
    alarms(modelData, fileout)  #liest sensoren[]
    #luactrl(modelData, fileout)            #inhalt unklar
    #iqsdata(modelData, fileout)            #inhalt unklar
    #commands(modelData, fileout)           #inhalt unklar
    #accel(modelData, fileout)              #bewegunssensoren, unklar wie zu erkennen ob definiert oder nur default werte, DC16?
    #audio(modelData, fileout)              #schalter zum audio files abspielen?
    #voicerec(modelData, fileout)           #sprachaufname ?
    #usermenu(modelData, fileout)           #keine prio


#------------------------     funktion zum selektieren der modell dateien     ----------------------------------
def selectInput():

    global csvOpt
    
    initdir = os.getcwd()

    filelist = filedialog.askopenfiles(
        mode='r',
        title='eine oder mehrere jsn Modell Dateien auswählen',
        initialdir=initdir,
        filetypes=[('jsn Dateien', ['.jsn'])],
        multiple=True)
    if not filelist:
        return None

    for item in filelist:
        fileName = item.name  # voller name ab root bzw laufwerk
        print('\ninput', fileName)
        # input encoding UTF-8 für portabilität bzgl umlaute (standard für python u.a.)
        # input daten ebenfalls in UTF-8 erwartet, zeichen die es nicht sind wie hex B0 als grad in telemetrie
        # werden beim einlesen durch � ersetzt (durch errors='replace')
        try:
            with open(fileName, 'r', encoding='utf-8',
                      errors='replace') as filein:
                try:
                    modelData = json.load(filein)  # ergebnis modelData ist dict
                except json.decoder.JSONDecodeError as e:
                    print('Datei', fileName, 'ist kein gültiges Modell\n', e)
                    out = 'Datei ' + fileName + ' ist kein gültiges Modell\n' + str(e)
                    tk.messagebox.showinfo(title='jemoview', message=out)
                    continue
        except OSError as e:
            print('Datei', fileName, 'nicht lesbar\n', e)
            out = 'Datei ' + fileName, ' nicht lesbar\n' + str(e)
            tk.messagebox.showinfo(title='jemoview', message=out)
            continue
        filein.close()
        if 'Global' not in modelData:
            print('Datei', fileName, 'ist kein gültiges Modell')
            out = 'Datei ' + fileName + ' ist kein gültiges Modell'
            tk.messagebox.showinfo(title='jemoview', message=out)
            continue

        # prüfen wo ergebnis zu speichern ist
        filecsv = fileName.replace('.jsn', '.csv')
        basNam = os.path.basename(filecsv)
        dirNam = os.path.dirname(filecsv)
        dirNamCsv = dirNam + os.path.sep + 'csv'
        if csvOpt.get() == 1:
            filecsv = dirNamCsv + os.path.sep + basNam
            if not os.path.exists(dirNamCsv):
                try:
                    os.mkdir(dirNamCsv)
                except OSError as e:
                    print('konnte Unterordner csv nicht anlegen', e)
                    out = 'konnte Unterordner csv nicht anlegen\n' + str(e)
                    tk.messagebox.showinfo(title='jemoview', message=out)
                    continue
        # output
        try:
            with open(filecsv, 'w', encoding='utf-8',
                      errors='replace') as fileout:
                fileout.write(version)
                # jetzt auswerten
                extract(modelData, fileout)
                fileout.write('\n')
        except OSError as e:
            print('Datei', filecsv, 'nicht schreibbar\n', e)
            out = 'Datei ' + filecsv + ' nicht schreibbar\n' + str(e)
            tk.messagebox.showinfo(title='jemoview', message=out)
            continue
        print('output', filecsv)
        fileout.close()

    tk.messagebox.showinfo(title='jemoview',
                           message='bereit für weitere Modelle')
    return


#------------------------     funktion for exit     ----------------------------------
def finishIt():
    sys.exit()


#------------------------------------     main   loop -------------------

app = tk.Tk()
app.title(version)

# Create a canvas
app.geometry('400x300+400+300')

tk.Label(app, text=' ', font=('Times', 5, 'bold'), width=50, fg='black').pack()

# csv option radiobuttons
csvOpt = IntVar()
csvOpt.set(0)
tk.Label(app,
         text='wo sollen die csv Ergebnis Dateien gespeichert werden:',
         padx=20).pack()
tk.Radiobutton(app,
               text='+  im selben Ordner wie Model Datei speichern',
               indicatoron=0,
               width=40,
               padx=5,
               variable=csvOpt,
               value=0).pack()

tk.Radiobutton(app,
               text='+  in Unterordner csv von Model Datei Ordner    ',
               indicatoron=0,
               width=40,
               padx=5,
               variable=csvOpt,
               value=1).pack()

tk.Label(app, text=' ', font=('Times', 5, 'bold'), width=50, fg='black').pack()

# start button
tk.Button(app,
          text='Start',
          font=('Times', 20, 'bold'),
          width=50,
          fg='blue',
          padx=40,
          pady=40,
          command=lambda: selectInput()).pack()

# exit button
tk.Button(app,
          text='Exit',
          font=('Times', 20, 'bold'),
          width=50,
          fg='red',
          padx=20,
          pady=20,
          command=lambda: finishIt()).pack()

app.mainloop()
