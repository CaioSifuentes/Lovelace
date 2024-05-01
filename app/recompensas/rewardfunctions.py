class RewardFunctions:
        @staticmethod
        def dnd(na: int):
            recompensasDeD = {
                2: 75,
                3: 100,
                4: 150,
                5: 200,
                6: 275,
                7: 400,
                8: 525,
                9: 650,
                10: 775,
                11: 900,
                12: 1200,
                13: 3000,
                14: 5000,
                15: 7500,
                16: 10000,
                17: 12500,
                18: 15000,
                19: 17500,
                20: 20000
            }

            return f'```(NA{na} | {recompensasDeD[na]}PO)```'
        
        @staticmethod
        def t20(nd: int, porcentagem: int):
            recompensasT20 = {
                1: [250, 50],
                2: [500, 75],
                3: [750, 100],
                4: [1000, 250],
                5: [1250, 375],
                6: [1500, 500],
                7: [1750, 625],
                8: [2000, 750],
                9: [2250, 1000],
                10: [2500, 1500],
                11: [2750, 2000],
                12: [3000, 2500],
                13: [3250, 3250],
                14: [3500, 4250],
                15: [3750, 5500],
                16: [4000, 7750],
                17: [4250, 10000],
                18: [4500, 12500],
                19: [4750, 15000],
                20: [5000, 18000]
            }

            tibares_total = int(recompensasT20[nd][1] * (porcentagem + 100) / 100)
            experiencia_total = int(recompensasT20[nd][0] * (porcentagem + 100) / 100)

            return f'```(ND{nd}+{porcentagem}%/{experiencia_total}XP | T${tibares_total})```'