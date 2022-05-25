---
title: GAMES101作业笔记
date: 2022-05-25 17:28:42
updated: 2022-05-25 17:28:42
top_img: false
cover: false
categories:
- 图形学
tags: 
- 图形学
description: GAMES101作业笔记
keywords: "CG, 图形学"
---

#### 一、作业1
要求：
每次作业的评分，分为基础与提高两部分，即在作业批改时会给大家反馈两
个成绩。由于作业不是强制要求必须提交，所以在完成全部作业后，我们会统计
所有的基础分数。若基础分数及格则视为通过课程，反之视为不通过。
• [5 分] 正确构建模型矩阵。
• [5 分] 正确构建透视投影矩阵。
• [10 分] 你的代码可以在现有框架下正确运行，并能看到变换后的三角形。
• [10 分] 当按A 键与D 键时，三角形能正确旋转。或者正确使用命令行得
到旋转结果图像。
• [提高项5 分] 在main.cpp 中构造一个函数，该函数的作用是得到绕任意
过原点的轴的旋转变换矩阵。
Eigen::Matrix4f get_rotation(Vector3f axis, float angle)

```c++
//实现：

Eigen::Matrix4f get_model_matrix(Axis targetAxis, float rotation_angle)
{
    Eigen::Matrix4f model = Eigen::Matrix4f::Identity();

    float angle_rad = rotation_angle * MY_PI / 180.0;

    Eigen::Matrix4f model_trans;
    if (targetAxis == AxisZ) {
        model_trans <<
            cos(angle_rad), -sin(angle_rad), 0, 0,
            sin(angle_rad), cos(angle_rad), 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1;
    }else if (targetAxis == AxisY) {
        model_trans <<
            cos(angle_rad), 0, sin(angle_rad), 0,
            0, 1, 0, 0,
            -sin(angle_rad), 0, cos(angle_rad), 0,
            0, 0, 0, 1;
    }
    else if (targetAxis == AxisX) {
        model_trans <<
            1, 0, 0, 0,
            0, cos(angle_rad), -sin(angle_rad), 0,
            0, sin(angle_rad), cos(angle_rad), 0,
            0, 0, 0, 1;
    }
    

    model = model_trans * model;

    return model;
}

Eigen::Matrix4f get_projection_matrix(float eye_fov, float aspect_ratio,
                                      float zNear, float zFar)
{
    float eye_fov_rad = eye_fov * MY_PI / 180.0;
    Eigen::Matrix4f projection = Eigen::Matrix4f::Identity();

    // Calc to get l, r, t, b
    float l, r, t, b;
    t = -tan(eye_fov_rad) * zNear; //这里要取反方向，不然会转过来
    b = -t;
    l = t * aspect_ratio;
    r = -l;

    // Construct Matrix(persp-ortho) 挤压(透视)变换
    Eigen::Matrix4f matrix_p2o;
    matrix_p2o << 
        zNear, 0, 0, 0,
        0, zNear, 0, 0,
        0, 0, zNear+zFar, -zNear*zFar,
        0, 0, 1, 0;

    // Construct Matrix(orth) 正交变换矩阵,先平移，后缩放
    Eigen::Matrix4f matrix_orth, matrix_orth_move, matrix_orth_scale;
    matrix_orth_move << 
        1,0,0, -(r+l)/2,
        0,1,0, -(t+b)/2,
        0,0,1, -(zNear+zFar)/2,
        0,0,0,1;
    matrix_orth_scale <<
        2/(r-l), 0, 0, 0,
        0, 2/(t-b), 0, 0,
        0, 0, 2/(zNear-zFar),0,
        0,0,0,1;

    matrix_orth = matrix_orth_move * matrix_orth_scale;

    //Calc to the result
    projection = matrix_orth * matrix_p2o;

    return projection;
}

```

#### 二、作业2
要求
• [5 分] 正确地提交所有必须的文件，且代码能够编译运行。
• [20 分] 正确实现三角形栅格化算法。
• [10 分] 正确测试点是否在三角形内。
• [10 分] 正确实现z-buffer 算法, 将三角形按顺序画在屏幕上。
• [提高项5 分] 用super-sampling 处理Anti-aliasing : 你可能会注意
到，当我们放大图像时，图像边缘会有锯齿感。我们可以用super-sampling
来解决这个问题，即对每个像素进行2 * 2 采样，并比较前后的结果(这里
并不需要考虑像素与像素间的样本复用)。需要注意的点有，对于像素内的每
一个样本都需要维护它自己的深度值，即每一个像素都需要维护一个sample
list。最后，如果你实现正确的话，你得到的三角形不应该有不正常的黑边。

```c++
static bool insideTriangle(float x, float y, const Vector3f* _v)
{   
    //Implement this function to check if the point (x, y) is inside the triangle represented by _v[0], _v[1], _v[2]
    Vector2f vec1 = Vector2f(x - _v[0].x(), y - _v[0].y());
    Vector2f edge1 = Vector2f(_v[1].x() - _v[0].x(), _v[1].y() - _v[0].y());

    Vector2f vec2 = Vector2f(x - _v[1].x(), y - _v[1].y());
    Vector2f edge2 = Vector2f(_v[2].x() - _v[1].x(), _v[2].y() - _v[1].y());

    Vector2f vec3 = Vector2f(x - _v[2].x(), y - _v[2].y());
    Vector2f edge3 = Vector2f(_v[0].x() - _v[2].x(), _v[0].y() - _v[2].y());

    return vec1[0] * edge1[1] - vec1[1] * edge1[0] > 0
        && vec2[0] * edge2[1] - vec2[1] * edge2[0] > 0
        && vec3[0] * edge3[1] - vec3[1] * edge3[0] > 0;
}

void rst::rasterizer::rasterize_triangle(const Triangle& t) {
    auto v = t.toVector4();
    
    // TODO : Find out the bounding box of current triangle.
    int min_x = std::floor(std::min(v[0][0], std::min(v[1][0], v[2][0])));
    int max_x = std::ceil(std::max(v[0][0], std::max(v[1][0], v[2][0])));
    int min_y = std::floor(std::min(v[0][1], std::min(v[1][1], v[2][1])));
    int max_y = std::ceil(std::max(v[0][1], std::max(v[1][1], v[2][1])));

    bool useMSAA = true;
    int msaaRate = 2;
    if (useMSAA) {
        std::vector<Vector2f> pos;

        float cell_size = 1.0 / msaaRate;
        for(int i = 0; i < msaaRate; i++)
        {
            for (int j = 0; j < msaaRate; j++)
            {
                pos.push_back({cell_size * (float)j + 0.5 * cell_size, cell_size * (float)i + 0.5 * cell_size});
            }
        }

        int inside_counter = 0;
        float min_depth, alpha, beta, gamma;
        
        for (int x = min_x; x <= max_x; x++)
        {
            for (int y = min_y; y < max_y; y++)
            {
                min_depth = FLT_MAX;
                inside_counter = 0;
                for (int part = 0; part < msaaRate*2; part++) {
                    Vector2f cur_point;
                    cur_point << static_cast<float>(x + pos[part][0]), static_cast<float>(y + pos[part][1]);
                    if (insideTriangle(cur_point.x(), cur_point.y(), t.v)) {
                        auto tup = computeBarycentric2D(cur_point.x(), cur_point.y(), t.v);
                        std::tie(alpha, beta, gamma) = tup;
                        float w_reciprocal = 1.0 / (alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
                        float z_interpolated = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
                        z_interpolated *= w_reciprocal;
                        min_depth = std::min(min_depth, z_interpolated);
                        inside_counter ++;
                    }
                }
                if (inside_counter > 0) {
                    if (depth_buf[get_index(x, y)] > min_depth) {
                        Vector3f point;
                        Eigen::Vector3f color = t.getColor() * inside_counter / (msaaRate * 2.0);
                        point << (float)x, (float)y, min_depth;
                        depth_buf[get_index(x, y)] = min_depth;
                        set_pixel(point, color);// 由count决定深浅
                    }
                }
            }
        }
    }
    else {
        float alpha, beta, gamma;
        for (int x = min_x; x <= max_x; x++)
        {
            for (int y = min_y; y < max_y; y++)
            {
                if (insideTriangle(static_cast<float>(x+0.5), static_cast<float>(y + 0.5), t.v)) {
                    auto tup = computeBarycentric2D(static_cast<float>(x + 0.5), static_cast<float>(y + 0.5), t.v);
                    std::tie(alpha, beta, gamma) = tup;
                    float w_reciprocal = 1.0 / (alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
                    float z_interpolated = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
                    z_interpolated *= w_reciprocal;

                    if (depth_buf[get_index(x, y)] > z_interpolated) {
                        Vector3f point;
                        point << static_cast<float>(x), static_cast<float>(y), z_interpolated;
                        depth_buf[get_index(x, y)] = z_interpolated;
                        set_pixel(point, t.getColor());
                    }
                }

            }
        }
    }
}


```

![效果对比](/img/160880489472852501.png) 