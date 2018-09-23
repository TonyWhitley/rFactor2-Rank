import unittest
import parse_record_files

f1_67_cch = r"""//[[gMa1.002f (c)2016    ]] [[            ]]
[CAREER]
Experience=2970
Money=5002970
CurSeasIndex=0
SinglePlayerVehicle="C:\Program Files (x86)\Steam\steamapps\common\rFactor 2\Installed\Vehicles\Brabham_BT20_1966\1.8\BT20_3.VEH"
SinglePlayerFilter="Brabham_BT20"
MultiPlayerFilter="|Brabham_BT20|EVE_F1|EVE_F1B|EVE_F1C|EVE_F2|EVE_F3|EVE_F3B|F167|Spark_F1|Spark_F2|Spark_F2B|Spark_F3"
AIAggression=0.0381
SinglePlayerAIStrength=105
MultiPlayerAIStrength=95
AbortedSeasons=0
TotalLaps=81
TotalRaces=14
TotalRacesWithAI=14
TotalPointsScored=9
TotalChampionships=0
TotalWins=1
TotalPoles=0
TotalLapRecords=0
AvgStartPosition=3.571429
AvgFinishPosition=7.057143
AvgRaceDistance=12.857142
AvgOpponentStrength=102.142860
[PLAYERTRACKSTAT]
TrackName=MONTECARLO_1966
TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\MONTECARLO_1966\2.1\MONTECARLO_1966
ClassRecord="*",6,95.6254,-1.0000,-1.0000
ClassRecord="Brabham BT20",6,95.6254,-1.0000,-1.0000
CRL="BT20 #3","Bias-Ply","Bias-Ply",25332273,4278124029,758005776
AIParameters="Brabham BT20",100.0000,0.0381,0.0476,0
AIParameters="Pace Car",-1.0000,-1.0000,-1.0000,0
[PLAYERTRACKSTAT]
TrackName=AUTODROMO_DI_IMOLA_GP
TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\SM_AUTODROMO_DI_IMOLA_V1.2\1.2\AUTODROMO_DI_IMOLA_GP
AIParameters="Brabham BT20",100.0000,0.0381,0.0476,0
[PLAYERTRACKSTAT]
TrackName=ROUEN 1955-70
TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\VLM_ROUEN-LES-ESSARTS_SJ.DD\0.97\ROUEN 1955-70
ClassRecord="*",43,124.3666,-1.0000,124.3666
ClassRecord="Ferrari 312/67 Ferrari 242 3.0 ",37,124.3666,-1.0000,124.3666
CRL="Ferrari 312/67 #20 ","Firestone","Firestone",25256066,4177196537,586268688
CRR="Ferrari 312/67 #20 ","Firestone","Firestone",25256066,4177196537,586268688
ClassRecord="Brabham BT20",6,128.0244,-1.0000,128.0244
CRL="BT20 #3","Bias-Ply","Bias-Ply",25333673,4261346813,1512980496
CRR="BT20 #3","Bias-Ply","Bias-Ply",25333673,4261346813,1512980496
AIParameters="Ferrari 312/67 Ferrari 242 3.0 ",100.0000,0.0381,0.0476,0
AIParameters="Pace Car",-1.0000,-1.0000,-1.0000,0
AIParameters="EVE_F1",-1.0000,-1.0000,-1.0000,0
AIParameters="Brabham BT20",100.0000,0.0381,0.0476,0
AIParameters="Spark_F1",-1.0000,-1.0000,-1.0000,0
[PLAYERTRACKSTAT]
TrackName=KYALAMI_LEGENDS
TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\SM_KYALAMI_LEGENDS_V1.01LE\1.01LE\KYALAMI_LEGENDS
ClassRecord="*",32,84.0992,-1.0000,84.0992
ClassRecord="Brabham BT20",32,84.0992,-1.0000,84.0992
CRL="BT20 #2","Bias-Ply","Bias-Ply",25235743,4261346813,300580864
CRR="BT20 #2","Bias-Ply","Bias-Ply",25235743,4261346813,300580864
AIParameters="Pace Car",-1.0000,-1.0000,-1.0000,0
AIParameters="Brabham BT20",100.0000,0.0381,0.0476,0
AIParameters="Ferrari 312/67 Ferrari 242 3.0 ",100.0000,0.0381,0.0476,0
AIParameters="EVE_F1",100.0000,0.0381,0.0476,0
AIParameters="Spark_F1",100.0000,0.0381,0.0476,0

"""
record1_result = r"""[PLAYERTRACKSTAT]
TrackName=MONTECARLO_1966
TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\MONTECARLO_1966\2.1\MONTECARLO_1966
ClassRecord="*",6,95.6254,-1.0000,-1.0000
ClassRecord="Brabham BT20",6,95.6254,-1.0000,-1.0000
"""

record2_result = None
record2_error = r"""WARNING: Something's wrong with a PLAYERTRACKSTAT entry
in file f1_67_cch at line 33, please check.
Keywords "TrackName" and / or "ClassRecord" not found
where I expected them:
f1_67_cch:33: [PLAYERTRACKSTAT]
f1_67_cch:34: TrackName=AUTODROMO_DI_IMOLA_GP
f1_67_cch:35: TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFAC...
f1_67_cch:36: AIParameters="Brabham BT20",100.0000,0.0381,0.0476,0
"""

record3_result = r"""[PLAYERTRACKSTAT]
TrackName=ROUEN 1955-70
TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\VLM_ROUEN-LES-ESSARTS_SJ.DD\0.97\ROUEN 1955-70
ClassRecord="*",43,124.3666,-1.0000,124.3666
ClassRecord="Ferrari 312/67 Ferrari 242 3.0 ",37,124.3666,-1.0000,124.3666
ClassRecord="Brabham BT20",6,128.0244,-1.0000,128.0244
"""

career_blt_result = r"""[PLAYERTRACKSTAT]
TrackName=MONTECARLO_1966
TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\MONTECARLO_1966\2.1\MONTECARLO_1966
ClassRecord="*",6,95.6254,-1.0000,-1.0000
ClassRecord="Brabham BT20",6,95.6254,-1.0000,-1.0000
[PLAYERTRACKSTAT]
TrackName=ROUEN 1955-70
TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\VLM_ROUEN-LES-ESSARTS_SJ.DD\0.97\ROUEN 1955-70
ClassRecord="*",43,124.3666,-1.0000,124.3666
ClassRecord="Ferrari 312/67 Ferrari 242 3.0 ",37,124.3666,-1.0000,124.3666
ClassRecord="Brabham BT20",6,128.0244,-1.0000,128.0244
[PLAYERTRACKSTAT]
TrackName=KYALAMI_LEGENDS
TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\SM_KYALAMI_LEGENDS_V1.01LE\1.01LE\KYALAMI_LEGENDS
ClassRecord="*",32,84.0992,-1.0000,84.0992
ClassRecord="Brabham BT20",32,84.0992,-1.0000,84.0992
"""

blankTractStat = r"""//[[gMa1.002f (c)2016    ]] [[            ]]
[CAREER]
Experience=2970
...blah...
[PLAYERTRACKSTAT]
TrackName=AUTODROMO_DI_IMOLA_GP
TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFACTOR 2\INSTALLED\LOCATIONS\SM_AUTODROMO_DI_IMOLA_V1.2\1.2\AUTODROMO_DI_IMOLA_GP
AIParameters="Brabham BT20",100.0000,0.0381,0.0476,0
"""

blankTractStatError = r"""WARNING: Something's wrong with a PLAYERTRACKSTAT entry
in file blankTractStat at line 5, please check.
Keywords "TrackName" and / or "ClassRecord" not found
where I expected them:
blankTractStat:5: [PLAYERTRACKSTAT]
blankTractStat:6: TrackName=AUTODROMO_DI_IMOLA_GP
blankTractStat:7: TrackFile=C:\PROGRAM FILES (X86)\STEAM\STEAMAPPS\COMMON\RFAC...
blankTractStat:8: AIParameters="Brabham BT20",100.0000,0.0381,0.0476,0
"""


class Test_test1(unittest.TestCase):
    def test_1_splitIntoRecords(self):
        cchFile_o = parse_record_files.cchFile(f1_67_cch, 'f1_67_cch')
        self.assertEqual(len(cchFile_o.recordsText), 5)

    def test_2_contentsOfRecord1(self):
        cchFile_o = parse_record_files.cchFile(f1_67_cch, 'f1_67_cch')
        self.assertEqual(len(cchFile_o.records[1]), 8)

    def test_3_resultOfRecord1(self):
        cchFile_o = parse_record_files.cchFile(f1_67_cch, 'f1_67_cch')
        #print(cchFile_o.recordResults[1])
        #print(len(cchFile_o.recordResults[1]))
        #print(record1_result)
        #print(len(record1_result))
        self.assertMultiLineEqual(cchFile_o.recordResults[1][0], record1_result)

    def test_4_resultOfRecord2(self):
        cchFile_o = parse_record_files.cchFile(f1_67_cch, 'f1_67_cch')
        self.assertEqual(cchFile_o.recordResults[2][0], record2_result)

    def test_4e_errorsOfRecord2(self):
        cchFile_o = parse_record_files.cchFile(f1_67_cch, 'f1_67_cch')
        print(cchFile_o.recordResults[2][1])
        self.assertMultiLineEqual(cchFile_o.recordResults[2][1], record2_error)

    def test_5_resultOfRecord3(self):
        cchFile_o = parse_record_files.cchFile(f1_67_cch, 'f1_67_cch')
        self.assertMultiLineEqual(cchFile_o.recordResults[3][0], record3_result)

    def test_6_resultOfAllRecords(self):
        cchFile_o = parse_record_files.cchFile(f1_67_cch, 'f1_67_cch')
        _career_blt = cchFile_o.get_career_blt_contribution()
        print(_career_blt)
        self.assertMultiLineEqual(_career_blt, career_blt_result)

        _errors = cchFile_o.get_errors()
        self.assertMultiLineEqual(_errors, record2_error)

    def test_7_resultOfAllRecords_blank(self):
        cchFile_o = parse_record_files.cchFile(blankTractStat, 'blankTractStat')
        _career_blt = cchFile_o.get_career_blt_contribution()
        self.assertMultiLineEqual(_career_blt, '')

        _errors = cchFile_o.get_errors()
        self.assertMultiLineEqual(_errors, blankTractStatError)

if __name__ == '__main__':
    unittest.main()
