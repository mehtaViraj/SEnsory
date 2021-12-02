import movement.servo_handler as servo_handler
import movement.ultrasonic_sensors as ultrasonic_sensors
import time
import movement.colour.colour_in_shape_filtered as cl


class Pathfinding:
    def __init__(self):
        # print("INITIALIZING")
        self.THRESHOLD_DISTANCE = 50

        self.ultra = ultrasonic_sensors.UltrasonicHandler(
            [38, 40], [37, 35], [29, 31])
        self.ultra.start_measuring()

        self.servo = servo_handler.ServoHandler(23, 21)
        self.cam = cl.CameraHandler("192.168.245.236")

        self.coordinates = []
        self.moves = []
        self.indexes = []
        self.colour = ""

        self.pic_count = 0
        # print("INITIALIZED")

    # def reserve_servo(self):
        #self.servo=servo_handler.ServoHandler(23, 21)

    def release_all(self):
        if self.servo != None:
            self.servo.release()
            self.cam.release()
            self.ultra.release()
            print('All hardware released')

    def test(self, seconds, cycle):
        #servo = SH.ServoHandler(21,23)
        self.servo.move_forever(cycle)
        time.sleep(seconds)
        self.servo.stop_move_forever()
        # servo.release()

    def calibrate(self, seconds):
        self.servo.calibrate_loop(seconds)

    def rotate_away(self, num):
        if num == 1:
            self.servo.rotate(5)  # turn left
        elif num == 0:
            self.servo.rotate(5)  # turn right

    def left_turn(self, ):
        self.servo.rotate(90)
        #indicator = 0

    def right_turn(self, ):
        # if distance from the front and left are small
        self.servo.rotate(-90)
        #indicator = 0

    def check_coordinates(self, coordinates, turn_indicator):

        print("Reached Check Coordinates")

        if len(coordinates) < 3:
            print("Initial Condition")
            self.servo.stop_move_forever()
            self.right_turn()
            self.moves.append("right")
            self.ultra.front = self.ultra._update_distance(
                self.ultra.front_trigger, self.ultra.front_echo)
            self.move_straight(self.colour)

        for i in range(len(coordinates)):
            coord_count = 0
            for j in range(len(coordinates)):
                # check the list for duplicate x co-ordinates
                if turn_indicator == 1:
                    print("Moving in x axis")
                    if coordinates[i][1][0] == coordinates[j][1][0]:
                        coord_count += 1

                # check the list for duplicate y co-ordinates
                if turn_indicator == 2:
                    print("Moving in y axis")
                    if coordinates[i][1][1] == coordinates[j][1][1]:
                        coord_count += 1

            if coord_count > 1:
                print("Found out bad direction")
                cur_coord = self.servo.pos
                self.servo.stop_move_forever()
                if cur_coord[0]-self.servo.pos[0] > 0:
                    self.servo.rotate(-90)
                    self.servo.append("right")

                    self.ultra.front = self.ultra._update_distance(
                        self.ultra.front_trigger, self.ultra.front_echo)
                    self.move_straight(self.colour)
                else:
                    self.servo.rotate(90)
                    self.ultra.front = self.ultra._update_distance(
                        self.ultra.front_trigger, self.ultra.front_echo)
                    self.move_straight(self.colour)

            else:
                self.right_turn()
                self.moves.append("right")

            self.indexes.append(len(self.moves)-1)

    def retrace(self, indexes):

        if len(indexes) == 0:
            print("Explored all of thr room")
            self.servo.stop_move_forever()
            return
        
        desired_index = indexes[-1]
        number_of_moves = (len(self.moves)-1)-desired_index

        self.servo.move_forever()
        for i in range(number_of_moves):

            if self.moves[len(self.moves)-i-1] == "right" and self.ultra.front < self.THRESHOLD_DISTANCE and self.ultra.right < self.THRESHOLD_DISTANCE:
                self.servo.stop_move_forever()
                self.left_turn()
                if i == number_of_moves-1:
                    self.servo.stop_move_forever()
                else:
                    self.servo.move_forever()
            elif self.moves[len(self.moves)-i-1] == "right" and self.ultra.front < self.THRESHOLD_DISTANCE and self.ultra.right < self.THRESHOLD_DISTANCE:
                self.servo.stop_move_forever()
                self.right_turn()
                if i == number_of_moves-1:
                    self.servo.stop_move_forever()
                else:
                    self.servo.move_forever()

    def move_straight(self, colour, robot_state=1, isFound=False):
        #global indicator
        # time.sleep(1)

        self.colour=colour

        self.servo.move_forever()

        turn_counter = 0

        while(self.ultra.front > self.THRESHOLD_DISTANCE):
            print("Front: "+str(self.ultra.front)
                  [:6]+" | Left: "+str(self.ultra.left)[:6]+"| Right: "+str(self.ultra.right)[:6]+"  -  NEW")
            try: 
                found_objects = self.cam.find_obj(colour)
            except KeyError:
                print("Excepted KeyError: No key '{}'".format(colour))
                return
            # print(found_objects)
            if self.pic_count >= 4:
                print('Found plenty of items, finishing.')
                return

            if not isFound and (len(found_objects) != 0):
                # servo.stop_move_forever()

                # del_file(r'/home/pi/sensory/SEnsory/flaskserver/movement/saved_images')
                # servo.stop_move_forever()
                self.cam.save_picture()
                isFound = True
                self.pic_count = self.pic_count + 1
                #move_straight(colour, 0, isFound)
            if isFound and (len(found_objects) == 0):
                isFound = False

            time.sleep(0.4)

        # moving right
        '''
        time_taken = 1
        time_count = 0

        if ultra.right <= 15:
            init_dist = ultra.right
            final_dist = 0
            while(final_dist - init_dist >= 0):
                time_start = time.time()
                rotate_away(1)
                if time.time() - time_start == 0.1:
                    init_dist = final_dist
                    final_dist = ultra.right

        if ultra.left <= 15:
            init_dist = ultra.left
            final_dist = 0
            while(final_dist - init_dist >= 0):
                time_start = time.time()
                rotate_away(0)
                if time.time() - time_start == 0.1:
                    init_dist = final_dist
                    final_dist = ultra.right'''

        if self.ultra.left <= self.THRESHOLD_DISTANCE and self.ultra.right > self.THRESHOLD_DISTANCE:
            print("Going right")
            self.servo.stop_move_forever()
            self.right_turn()
            self.moves.append("right")
            #indicator = 0
            self.ultra.front = self.ultra._update_distance(
                self.ultra.front_trigger, self.ultra.front_echo)
            self.move_straight(colour, isFound)

        # moving left
        elif self.ultra.right <= self.THRESHOLD_DISTANCE and self.ultra.left > self.THRESHOLD_DISTANCE:
            print("Going left")
            self.servo.stop_move_forever()
            self.left_turn()
            self.moves.append("left")
            print("Moves:")
            print(self.moves)
            #indicator = 0
            self.ultra.front = self.ultra._update_distance(
                self.ultra.front_trigger, self.ultra.front_echo)
            self.move_straight(colour, isFound)

        elif self.ultra.right > (self.THRESHOLD_DISTANCE) and self.ultra.left > (self.THRESHOLD_DISTANCE):
            '''print("Free space. Go right")
            coordinates.append([servo.pos, 90])
            print(coordinates)
            right_turn()
            #indicator = 0
            ultra.front = ultra._update_distance(
                ultra.front_trigger, ultra.front_echo)
            move_straight(colour, isFound)'''

            print("Free space. Take decision")
            # currently the y co-ordinate is changing
            if self.servo.heading % 180 == 0:
                # check the list for duplicate x co-ordinates
                self.check_coordinates(self.coordinates, 1)
            else:
                self.check_coordinates(self.coordinates, 2)

            self.coordinates.append([self.servo.pos, 90])
            print(self.coordinates)
            #indicator = 0
            self.ultra.front = self.ultra._update_distance(
                self.ultra.front_trigger, self.ultra.front_echo)
            self.move_straight(colour, isFound)

        elif self.ultra.right < self.THRESHOLD_DISTANCE and self.ultra.left < self.THRESHOLD_DISTANCE:
            print("Deadend. Retracing....")
            self.servo.stop_move_forever()
            self.servo.rotate(180)
            self.retrace(self.indexes)
            self.move_straight(colour, isFound)

        '''else:
            print("Free space. Go right")
            coordinates.append([servo.pos, 90])
            print(coordinates)

            right_turn()
            #indicator = 0
            #ultra.front = ultra._update_distance(ultra.front_trigger, ultra.front_echo)
            move_straight(colour, isFound)'''

        # while robot_state == 0:
        #     self.servo.stop_move_forever
