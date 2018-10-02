
int roomwidth = 1200;
int roomHeight = 800;
int depth = 800;
int poolSize = 9;
float localradius = 30;

PImage[] texturePool = new PImage[poolSize];
PImage wall, left, ceiling, right, floor;


ArrayList<Ball> balls;

final float gravity = 0.8;

class Ball {
  float x;
  float y;
  float z;
  float xVelocity;
  float yVelocity;
  float zVelocity;
  float radius;
  int textureIdx;
  PShape shape;

  Ball(float x, float y, float z, float xVelo, float yVelo, float zVelo, float radius, PShape shape) {
    this.x = x;
    this.y = y;
    this.z = z;
    this.xVelocity = xVelo;
    this.yVelocity = yVelo;
    this.zVelocity = zVelo;
    this.radius = radius;
    this.shape = shape;
  }

  void render() {
    pushMatrix();
    translate(this.x, this.y, this.z);
    shape(shape, 0, 0);
    popMatrix();

  }

  float getRadius() {return radius;}

  float getX() {return x;}

  float getY() {return y;}

  float getZ() {return z;}

  void setX(float x) {this.x = x;}

  void setY(float y) {this.y = y;}

  void setZ(float z) {this.z = z;}

  float getXVelo() {return this.xVelocity;}

  float getYVelo() {return this.yVelocity;}

  float getZVelo() {return this.zVelocity;}

  void setXVelo(float newx) {this.xVelocity = newx;}

  void setYVelo(float newy) {this.yVelocity = newy;}

  void setZVelo(float newz) {this.zVelocity = newz;}


  void move() {

    this.x = this.x + this.xVelocity;

    this.y = this.y + this.yVelocity;

    this.yVelocity++;

    this.z = this.z + this.zVelocity;

    //this.yVelocity = this.yVelocity * gravity;

    if (this.z - this.radius < -depth)
    {
      this.setZ(this.radius - depth);
      this.setZVelo(-this.zVelocity);
    }

    if (this.z  > 0)
    {
      this.setZ(0);
      this.setZVelo(-this.zVelocity);
    }

    if (this.x + this.radius> roomwidth)
    {
      this.setX(roomwidth - this.radius);
      this.setXVelo(-this.xVelocity);
    }

    if (this.x - this.radius < 0)
    {
      this.setX(this.radius);
      this.setXVelo(-this.xVelocity);
    }

    if (this.y + this.radius > roomHeight)
    {
      this.setY(roomHeight - this.radius);
      this.setYVelo(-gravity*this.yVelocity);
      //this.setYVelo(-this.yVelocity);
    }

    if (this.y - this.radius < 0)
    {
      this.setY(this.radius);
      this.setYVelo(-this.yVelocity);
    }

  }
}

void mousePressed() {
  // Get random texture index from the texturepool.
  float r = random(0, poolSize);
  int ir = int(r);

  PShape shape = createShape(SPHERE, localradius);

  // Get the texture img from texture pool based on the index.
  PImage img = texturePool[ir];
  shape.setTexture(img);
  shape.setStroke(false);

  Ball newball = new Ball(mouseX, mouseY, 0, random(-10, 10), random(-10, 10), -10, localradius, shape);
  balls.add(newball);

  println("New Ball " + newball.getZVelo());
  println("New Ball " + newball.getRadius());
  println("Balls size: " + balls.size());
}

void loadBackgroundImage()
{
  wall = loadImage("wall.jpg");
  left = loadImage("left.jpg");
  right = loadImage("left.jpg");
  ceiling = loadImage("ceiling.jpeg");
  floor = loadImage("floor.jpg");
}

void loadTexturePool()
{
  int texturecounter = 1;

  // Loading the all the textures into a texture pool.
  for (int i = 0; i < poolSize; i++) {
    String imageName = "randomTexture/" + str(texturecounter) + ".jpg";
    texturePool[i] = loadImage(imageName);
    texturecounter = texturecounter + 1;
  }
}

void setup() {
  size(1200, 800, P3D);
  background(100);

  loadTexturePool();

  loadBackgroundImage();

  balls = new ArrayList<Ball>();
}

void draw() {

  lights();
  background(100);

  //// Wall
  noStroke();
  beginShape();
  texture(wall);
  vertex(0, 0, -1*depth, 900, 0);
  vertex(width, 0, -1*depth, 0, 0);
  vertex(width, height, -1*depth, 0, 600);
  vertex(0, height, -1*depth, 900, 600);
  endShape();

  //// Left
  noStroke();
  beginShape();
  texture(left);
  vertex(0, 0, 0, 0, 0);
  vertex(0, 0, -1*depth, 626, 0);
  vertex(0, height, -1*depth, 626, 409);
  vertex(0, height, 0, 0, 409);
  endShape();

  //// Ceiling
  beginShape();
  texture(ceiling);
  vertex(0, 0, 0, 0, 0);
  vertex(width, 0, 0, 0, 280);
  vertex(width, 0, -1*depth, 280, 280);
  vertex(0, 0, -1*depth, 280, 0);
  endShape();

  // Right
  noStroke();
  beginShape();
  texture(right);
  vertex(width, 0, 0, 0, 0);
  vertex(width, 0, -1*depth, 626, 0);
  vertex(width, height, -1*depth, 626, 409);
  vertex(width, height, 0, 0, 409);
  endShape();

  //// Floor
  noStroke();
  beginShape();
  texture(floor);
  vertex(0, height, 0, 0, 0);
  vertex(width, height, 0, 1300, 0);
  vertex(width, height, -1*depth, 1300, 1012);
  vertex(0, height, -1*depth, 0, 1012);
  endShape();

  for (Ball b : balls) {
    b.render();
    b.move();
  }
}
