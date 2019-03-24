import time
start_time = time.time()

import pandas as pd
import random

def filterPosition(position):
    ppdQuantile = position.PPD.quantile(0.5)
    position = position[position.PPD > ppdQuantile]
    pointsQuantile = position.Points.quantile(0.2)
    position = position[position.Points > pointsQuantile]
    return position

def createPositionLineup(position, positionDataFrame, lineupDataFrame):
    names = []
    for row1 in positionDataFrame.itertuples(index = False):
        for row2 in positionDataFrame.itertuples(index = False):
            # Doesn't add any combination of the same player
            if row1[0] != row2[0] and (str(row2[0] + row1[0])) not in names:
                    names.append(str(row1[0] + row2[0]))
                    # PPD is points per dollar, a measure of player value
                    pPoints = row1[1] + row2[1]
                    pSal = row1[2] + row2[2]
                    ppd = (row1[4] + row2[4])/2
                    lineup = pd.DataFrame([[position + "1: " + row1[0] + " " + position + "2: " + row2[0] + " ", pPoints, pSal, ppd]], columns = ["Name", "Points", "Salary", "PPD"])
                    lineupDataFrame = lineupDataFrame.append(lineup)

    lineupDataFrame.sort_values(by = "PPD", axis = 0, ascending = False, inplace = True)
    lineupDataFrame = lineupDataFrame.iloc[:20]
    print("Position Length:", len(lineupDataFrame))
    lineupDataFrame.reset_index(inplace = True)
    lineupDataFrame.drop(columns = 'index', inplace = True)
    return lineupDataFrame

def totalPtsEstimate(PGs, SGs, SFs, PFs, centers):

    q = 0.9999
    overallSal = PGs.Salary.quantile(q) + SGs.Salary.quantile(q) + SFs.Salary.quantile(q) + PFs.Salary.quantile(q) + centers.Salary.quantile(q)
    while overallSal > 60000:
        overallSal = PGs.Salary.quantile(q) + SGs.Salary.quantile(q) + SFs.Salary.quantile(q) + PFs.Salary.quantile(q) + centers.Salary.quantile(q)
        q -= 0.0001
    overallPts = PGs.Points.quantile(q) + SGs.Points.quantile(q) + SFs.Points.quantile(q) + PFs.Points.quantile(q) + centers.Points.quantile(q)
    print("Overall Points:", overallPts)
    return overallPts

def findBounds(PGs, SGs, SFs, PFs, centers):
    # I could use this sampling to get the lineup point and salary minimums by position and filter them before they go into the nested for loop
    # This would reduce the number of unnecessary iterations
    # However this would make sampling well even more important so a larger sample size may be necessary
    overallPts = totalPtsEstimate(PGs, SGs, SFs, PFs, centers)
    count = 0
    while count <= 30:
        pgPts = random.choice(PGs.Points)
        sgPts = random.choice(SGs.Points)
        sfPts = random.choice(SFs.Points)
        pfPts = random.choice(PFs.Points)
        cenPts = random.choice(centers.Points)
        sampPts = pgPts + sgPts + sfPts + pfPts + cenPts
        pgSal = random.choice(PGs.Salary)
        sgSal = random.choice(SGs.Salary)
        sfSal = random.choice(SFs.Salary)
        pfSal = random.choice(PFs.Salary)
        cenSal = random.choice(centers.Salary)
        sampSal = pgSal + sgSal + sfSal + pfSal + cenSal

        if sampPts >= overallPts and 59000 <= sampSal <= 60000:
            if count > 0:
                pgPtsMin = min(pgPts, pgPtsMin)
                sgPtsMin = min(sgPts, sgPtsMin)
                subset1PtsMin = min(pgPts + sgPts, subset1PtsMin)
                sfPtsMin = min(sfPts, sfPtsMin)
                subset2PtsMin = min(pgPts + sgPts + sfPts, subset2PtsMin)
                pfPtsMin = min(pfPts, pfPtsMin)
                subset3PtsMin = min(pgPts + sgPts + sfPts + pfPts, subset3PtsMin)
                cenPtsMin = min(cenPts, cenPtsMin)
                pgSalMin = min(pgSal, pgSalMin)
                pgSalMax = max(pgSal, pgSalMax)
                sgSalMin = min(sgSal, sgSalMin)
                sgSalMax = max(sgSal, sgSalMax)
                sfSalMin = min(sfSal, sfSalMin)
                sfSalMax = max(sfSal, sfSalMax)
                pfSalMin = min(pfSal, pfSalMin)
                pfSalMax = max(pfSal, pfSalMax)
                cenSalMin = min(cenSal, cenSalMin)
                cenSalMax = max(cenSal, cenSalMax)
                subset1SalMin = min(pgSal + sgSal, subset1SalMin)
                subset1SalMax = max(pgSal + sgSal, subset1SalMax)
                subset2SalMin = min(pgSal + sgSal + sfSal, subset2SalMin)
                subset2SalMax = max(pgSal + sgSal + sfSal, subset2SalMax)
                subset3SalMin = min(pgSal + sgSal + sfSal + pfSal, subset3SalMin)
                subset3SalMax = max(pgSal + sgSal + sfSal + pfSal, subset3SalMax)
                overallSalMin = min(pgSal + sgSal + sfSal + pfSal+ cenSal, overallSalMin)

            else:
                pgPtsMin = pgPts
                sgPtsMin = sgPts
                subset1PtsMin = pgPts + sgPts
                sfPtsMin = sfPts
                subset2PtsMin = subset1PtsMin + sfPts
                pfPtsMin = pfPts
                subset3PtsMin = subset2PtsMin + pfPts
                cenPtsMin = cenPts
                pgSalMin = pgSal
                pgSalMax = pgSal
                sgSalMin = sgSal
                sgSalMax = sgSal
                sfSalMin = sfSal
                sfSalMax = sfSal
                pfSalMin = pgSal
                pfSalMax = pgSal
                cenSalMin = cenSal
                cenSalMax = cenSal
                subset1SalMin = pgSal + sgSal
                subset1SalMax = pgSal + sgSal
                subset2SalMin = subset1SalMin + sfSal
                subset2SalMax = subset1SalMax + sfSal
                subset3SalMin = subset2SalMin + pfSal
                subset3SalMax = subset2SalMax + pfSal
                overallSalMin = subset3SalMin + cenSal

            count += 1
            print(count)

    PGs = PGs[PGs.Points >= pgPtsMin]
    SGs = SGs[SGs.Points >= sgPtsMin]
    SFs = SFs[SFs.Points >= sfPtsMin]
    PFs = PFs[PFs.Points >= pfPtsMin]
    centers = centers[centers.Points >= cenPtsMin]
    PGs = PGs[PGs.Salary <= pgSalMax]
    SGs = SGs[SGs.Salary <= sgSalMax]
    SFs = SFs[SFs.Salary <= sfSalMax]
    PFs = PFs[PFs.Salary <= pfSalMax]
    centers = centers[centers.Salary <= cenSalMax]
    PGs = PGs[PGs.Salary >= pgSalMin]
    SGs = SGs[SGs.Salary >= sgSalMin]
    SFs = SFs[SFs.Salary >= sfSalMin]
    PFs = PFs[PFs.Salary >= pfSalMin]
    centers = centers[centers.Salary >= cenSalMin]

    print("Lengths:", len(PGs), len(SGs), len(SFs), len(PFs), len(centers))

    print("PG Point Min", pgPtsMin)
    print("Subset 1 Point Min", subset1PtsMin)
    print("Subset 2 Point Min", subset2PtsMin)
    print("Subset 3 Point Min", subset3PtsMin)
    print("Subset 1 Sal Min", subset1SalMin)
    print("PG Sal Min", pgSalMin)
    print("PG Sal Max", pgSalMax)
    print("Subset 1 Sal Min", subset1SalMin)
    print("Subset 1 Sal Max", subset1SalMax)
    print("Subset 2 Sal Min", subset2SalMin)
    print("Subset 2 Sal Max", subset2SalMax)
    print("Subset 3 Sal Min", subset3SalMin)
    print("Subset 3 Sal Max", subset3SalMax)
    print("Overall Sal", overallSalMin)

    print("\n------%f------" % (time.time() - start_time))

    return PGs, SGs, SFs, PFs, centers, pgPtsMin, subset1PtsMin, pgSalMin, pgSalMax, subset1SalMin, subset1SalMax, subset2PtsMin,subset2SalMin, subset2SalMax, subset3PtsMin, subset3SalMin, subset3SalMax, overallSalMin, overallPts

def makeCombos(PGs, SGs, SFs, PFs, centers, combos):
    PGs, SGs, SFs, PFs, centers, pgPtsMin, sub1PtsMin, pgSalMin, pgSalMax, sub1SalMin, sub1SalMax, sub2PtsMin,sub2SalMin, sub2SalMax, sub3PtsMin, sub3SalMin, sub3SalMax, overallSal, overallPts = findBounds(PGs, SGs, SFs, PFs, centers)
    for row1 in PGs.itertuples(index = False):
        pts = row1[1]
        sal = row1[2]
        if pgSalMin <= sal <= pgSalMax and pts >= pgPtsMin:
            for row2 in SGs.itertuples(index = False):
                pts1 = row1[1] + row2[1]
                sal1 = row1[2] + row2[2]
                if sub1SalMin <= sal1 <= sub1SalMax and pts1 >= sub1PtsMin:
                    for row3 in SFs.itertuples(index = False):
                        pts2 = pts1 + row3[1]
                        sal2 = sal1 + row3[2]
                        if sub2SalMin <= sal2 <= sub2SalMax and pts2 >= sub2PtsMin:
                            for row4 in PFs.itertuples(index = False):
                                pts3 = pts2 + row4[1]
                                sal3 = sal2 + row4[2]
                                # Evaluates if best possible lineup excluding center could the performance top projections based on the top percentile
                                if sub3SalMin <= sal3 <= sub3SalMax and pts3 >= sub3PtsMin:
                                    for row5 in centers.itertuples(index = False):
                                        totalPts = pts3 + row5[1]
                                        totalSal = sal3 + row5[2]
                                        # Evaluates if lineup is at or below salary cap and if it meets the performance target
                                        # Only appends lineup is above condition is true
                                        if overallSal <= totalSal <= 60000 and totalPts >= overallPts:
                                            combo = {"Name": (row1[0] + row2[0] + row3[0] + row4[0] + "C: " + row5[0]), "Points": totalPts, "Salary": totalSal}
                                            combos = combos.append(combo, ignore_index = True, sort = False)

    return combos

def main():

    pg = pd.DataFrame(columns = ["Name", "Points", "Salary", "PPD"])
    sg = pd.DataFrame(columns = ["Name", "Points", "Salary", "PPD"])
    sf = pd.DataFrame(columns = ["Name", "Points", "Salary", "PPD"])
    pf = pd.DataFrame(columns = ["Name", "Points", "Salary", "PPD"])
    cen = pd.DataFrame(columns = ["Name", "Points", "Salary", "PPD"])

    # Imports player data from text file into pandas dataframe
    rotoProj = pd.read_csv("https://rotogrinders.com/projected-stats/nba-player.csv?site=fanduel", delimiter= ",", header = None, names = ["Name", "Salary", "Team", "Position", "Opposing", "Ceiling", "Floor", "Points"])

    # Removes unnecessary columns
    rotoProj = rotoProj.filter(items = ["Name", "Points", "Salary", "Position"])
    rotoProj.insert(loc = 4, column = "PPD", value = (rotoProj.Points/rotoProj.Salary))

    # Only retains players in the top 50% by points per dollar relative to other players of the same position
    # Establishes dataframes from source data by player position
    pg = pd.DataFrame(rotoProj[rotoProj.Position == "PG"])
    pg = filterPosition(pg)
    sg = pd.DataFrame(rotoProj[rotoProj.Position == "SG"])
    sg = filterPosition(sg)
    sf = pd.DataFrame(rotoProj[rotoProj.Position == "SF"])
    sf = filterPosition(sf)
    pf = pd.DataFrame(rotoProj[rotoProj.Position == "PF"])
    pf = filterPosition(pf)
    cen = pd.DataFrame(rotoProj[rotoProj.Position == "C"])
    cen = filterPosition(cen)
    print("Possible combinations:", len(pg) * len(sg) * len(sf) * len(pf) * len(cen))
    cen.reset_index(inplace = True)
    cen = cen.drop(columns = 'index')

    # Establishes pairs of players for each position except center
    pgLineup = pd.DataFrame(columns = ["Name", "Points", "Salary", "PPD"])
    sgLineup = pd.DataFrame(columns = ["Name", "Points", "Salary", "PPD"])
    sfLineup = pd.DataFrame(columns = ["Name", "Points", "Salary", "PPD"])
    pfLineup = pd.DataFrame(columns = ["Name", "Points", "Salary", "PPD"])
    pgLineup = createPositionLineup("PG", pg, pgLineup)
    sgLineup = createPositionLineup("SG", sg, sgLineup)
    sfLineup = createPositionLineup("SF", sf, sfLineup)
    pfLineup = createPositionLineup("PF", pf, pfLineup)

    combinations = pd.DataFrame(columns = ["Name", "Points", "Salary"])
    combinations = makeCombos(pgLineup, sgLineup, sfLineup, pfLineup, cen, combinations)

    # Retains only top 15 combinations by point value
    print("Combinations:", len(combinations))
    combinations.sort_values(by = "Points", ascending = False, inplace = True)
    combinations = combinations.iloc[:10]
    print(combinations)
    combinations.to_csv('/Users/nishantsinha/Documents/USC/Personal Projects/Fanduel/Combinations.txt', sep=",", index=False, header=["Lineups", "Points", "Salary"], line_terminator="\n\n")

    # Writes mean value of points to combination document
    mean = combinations.Points.mean()
    combos = open('/Users/nishantsinha/Documents/USC/Personal Projects/Fanduel/Combinations.txt', 'a')
    print("\n" + str(mean))
    print("Mean:", mean, file = combos)
    combos.close()

# Calls main
main()

# Prints time to run the program
print("\n------%f------" % (time.time() - start_time))