#include <queue>
#include <vector>
#include <algorithm>
#include <map>
#include <iostream>

/*
using namespace::std;

struct node
{
    int val = 0;
    int mask = 0;
    int dist;
};


//input graph = [

class Solution {
public:
    int shortestPathLength(vector<vector<int>>& graph) {

        queue<node*>q;
        int res = 0;
        for (int i = 0; i < graph.size(); i++)
        {
            node* t = new node();
            t->val = i;
            t->mask = ((1 << i));

            t->dist = 0;
            q.push(t);
            res = res | ((1 << i));
        }

        map<pair<int, pair<int, int>>, int>mp;

        while (q.size())
        {
            node* t = q.front();
            int val = t->val;
            int mask = t->mask;
            int dist = t->dist;
            q.pop();



            if (mask == res)
                return dist;

            if (mp[{val, { mask,dist }}] == 0)
            {
                for (auto x : graph[val])
                {
                    node* t = new node();
                    t->val = x;
                    t->mask = (mask | (1 << x));
                    t->dist = 1 + dist;
                    q.push(t);
                }
                mp[{val, { mask,dist }}] = 1;
            }
        }


        return 0;
    }
};
*/

//input: distance (distance to wall)

using namespace std;

bool isWall(int distance)
{
    if (distance < 5)
    {
        return true; 
    }
    return false; 
}

//to figure out room dimensions
/* distance 
*   1 - north 
*   2 - east 
*   3 - south 
*   4 - west
*/

//a = direction with respect to wall, b = direction with respect to robot
int convert(int a, int b)
{
    //convert for right turn
    if (b == 2)
    {
        a += 1;
        if (a == 5)
            a = 1;
    }

    //convert for left turn
    if (b == 3)
    {
        a -= 1;
        if (a == 0)
            a = 4;
    }

    //convert for back
    if (b == 4)
    {
        a += 2;
        if (a == 6)
            a = 2;
        if (a == 5)
            a = 1;
    }
    return a;
    //converst the direction with respec to robot to respect to room 
}

int turn(int a)
{
    return a;
}

struct room{
    int distance;
    int direction;
};

//withrespect to the robot; 
//1 forward
//2 right
//3 left 
//4 back

//need a way to pass first direction in 
int run(std::vector<struct room> dimension, int direction)
{
    if (isWall(distance_front))//checks if wall is ahead
    {
        //store direction of room;
        struct room temp = { distance, direction };
        dimension.push_back(temp);

        //stores distance traveled to array;
        if (!isWall(distance_right))
        {
            //turn right and go right
            turn(2);
            direction = convert(direction, 2);

        }
        else if (!isWall(distance_left))
        {
            //turn left and go left
            turn(3);
            direction = convert(direction, 3);
        }
        else
        {
            //turn around 
            turn(4);
            direction = convert(direction, 4);
            if (!isWall(distrance_front))
            {
                std::cout << "there are walls on 4 sides" << std::endl;
                return 10;
            }
        }
    }
    return 0; 
}





//spd of motor and using rotation to find distance traveled
//assume I have distance 
int main()
{
    std::vector<struct room> dimension;

    int direction = 2; // sets inital direciton with respect to the room; 
    
    int a = 0;
    while (a != 10)
    {
        //pass stuff through vector? 
        a = run(dimension, direction);
    }  
}