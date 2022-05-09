import csv

def main():
    file = open('../../../App/traffic_speed_prediction/Speedlimit.csv')
    csvreader = csv.DictReader(file)
    speed_limits = {}

    for row in csvreader:
        road_id = row['TIE']
        section_id = row['AOSA']
        speed = row['NOPRAJ']

        if speed_limits.get((road_id, section_id)) is None or speed < speed_limits[(road_id, section_id)]:
            speed_limits[(road_id, section_id)] = speed

    print(len(speed_limits))


if __name__ == '__main__':
    main()
