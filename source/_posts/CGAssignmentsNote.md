---
title: GAMES101作业笔记
cover: /img/160880489472852501.png
date: 2022-05-25 17:30:37
updated: 2022-09-13 16:41:59
top_img: false
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


#### 三、作业3
要求：
• [5 分] 提交格式正确，包括所有需要的文件。代码可以正常编译、执行。
• [10 分] 参数插值: 正确插值颜色、法向量、纹理坐标、位置(Shading Position)
并将它们传递给fragment_shader_payload.
• [20 分]Blinn-phong 反射模型: 正确实现phong_fragment_shader 对应的
反射模型。
• [5 分] Texture mapping: 将phong_fragment_shader 的代码拷贝到
texture_fragment_shader, 在此基础上正确实现Texture Mapping.
• [10 分] Bump mapping 与Displacement mapping: 正确实现Bump mapping
与Displacement mapping.
7
• [Bonus 3 分] 尝试更多模型: 找到其他可用的.obj 文件，提交渲染结果并
把模型保存在/models 目录下。这些模型也应该包含Vertex Normal 信息。
• [Bonus 5 分] 双线性纹理插值: 使用双线性插值进行纹理采样, 在Texture
类中实现一个新方法Vector3f getColorBilinear(float u, float v) 并
通过fragment shader 调用它。为了使双线性插值的效果更加明显，你应该
考虑选择更小的纹理图。请同时提交纹理插值与双线性纹理插值的结果，并
进行比较。

> 向量点积对应到矩阵的点乘，是对应项的相乘之和。 向量叉乘对应矩阵间的m行与n列对应相乘之和成为新的m,n项（矩阵相乘），结果是一个新矩阵
> Eigen库的cwiseProduct实现了矩阵点积，即对应项相乘得到新的项，要求两个矩阵行列数要一样!

* rasterizer.cpp
```C++
//Screen space rasterization
void rst::rasterizer::rasterize_triangle(const Triangle& t, const std::array<Eigen::Vector3f, 3>& view_pos) 
{
    // TODO: From your HW3, get the triangle rasterization code.
    // TODO: Inside your rasterization loop:
    //    * v[i].w() is the vertex view space depth value z.
    //    * Z is interpolated view space depth for the current pixel
    //    * zp is depth between zNear and zFar, used for z-buffer

    // float Z = 1.0 / (alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
    // float zp = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
    // zp *= Z;

    // TODO: Interpolate the attributes:
    // auto interpolated_color
    // auto interpolated_normal
    // auto interpolated_texcoords
    // auto interpolated_shadingcoords

    // Use: fragment_shader_payload payload( interpolated_color, interpolated_normal.normalized(), interpolated_texcoords, texture ? &*texture : nullptr);
    // Use: payload.view_pos = interpolated_shadingcoords;
    // Use: Instead of passing the triangle's color directly to the frame buffer, pass the color to the shaders first to get the final color;
    // Use: auto pixel_color = fragment_shader(payload);

    auto v = t.toVector4();

    // TODO : Find out the bounding box of current triangle.
    int min_x = std::floor(std::min(v[0][0], std::min(v[1][0], v[2][0])));
    int max_x = std::ceil(std::max(v[0][0], std::max(v[1][0], v[2][0])));
    int min_y = std::floor(std::min(v[0][1], std::min(v[1][1], v[2][1])));
    int max_y = std::ceil(std::max(v[0][1], std::max(v[1][1], v[2][1])));

    int msaaRate = 2;
    float alpha, beta, gamma;
    for (int x = min_x; x <= max_x; x++)
    {
        for (int y = min_y; y < max_y; y++)
        {
            if (insideTriangle(static_cast<float>(x + 0.5), static_cast<float>(y + 0.5), t.v)) {
                auto tup = computeBarycentric2D(static_cast<float>(x + 0.5), static_cast<float>(y + 0.5), t.v);
                std::tie(alpha, beta, gamma) = tup;
                float w_reciprocal = 1.0 / (alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
                float z_interpolated = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
                z_interpolated *= w_reciprocal;

                if (depth_buf[get_index(x, y)] > z_interpolated) {
                    // TODO: Interpolate the attributes:
                     auto interpolated_color = interpolate(alpha, beta, gamma, t.color[0], t.color[1], t.color[2], 1);
                     auto interpolated_normal = interpolate(alpha, beta, gamma, t.normal[0], t.normal[1], t.normal[2], 1).normalized();
                     auto interpolated_texcoords = interpolate(alpha, beta, gamma, t.tex_coords[0], t.tex_coords[1], t.tex_coords[2], 1);
                     auto interpolated_shadingcoords = interpolate(alpha, beta, gamma, view_pos[0], view_pos[1], view_pos[2], 1);

                    fragment_shader_payload payload( interpolated_color, interpolated_normal.normalized(), interpolated_texcoords, texture ? &*texture : nullptr);
                    payload.view_pos = interpolated_shadingcoords;
                    auto pixel_color = fragment_shader(payload);

                    depth_buf[get_index(x, y)] = z_interpolated;
                    set_pixel(Eigen::Vector2i(x, y), pixel_color);
                }
            }

        }
    }
}
```

* Texture.hpp
```c++
  Eigen::Vector3f getColor(float u, float v)
    {
        // 坐标限定
       /* if (u < 0) u = 0;
        if (u > 1) u = 1;
        if (v < 0) v = 0;
        if (v > 1) v = 1;*/

        if (u < 0 || u > 1 || v < 0 || v > 1)
            return Eigen::Vector3f(0,0,0);
        auto u_img = u * width;
        auto v_img = (1 - v) * height;
        auto color = image_data.at<cv::Vec3b>(v_img, u_img);
        return Eigen::Vector3f(color[0], color[1], color[2]);

    }

    Eigen::Vector3f getColorBilinear(float u, float v)
    {
        if (u < 0) u = 0;
        if (u > 1) u = 1;
        if (v < 0) v = 0;
        if (v > 1) v = 1;
        auto u_img = u * width;
        auto v_img = (1 - v) * height;

        float u_min = std::floor(u_img);
        float u_max = std::min((float)width, std::ceil(u_img));
        float v_min = std::floor(v_img);
        float v_max = std::min((float)height, std::ceil(v_img));

        auto Q11 = image_data.at<cv::Vec3b>(v_max, u_min);
        auto Q12 = image_data.at<cv::Vec3b>(v_max, u_max);

        auto Q21 = image_data.at<cv::Vec3b>(v_min, u_min);
        auto Q22 = image_data.at<cv::Vec3b>(v_min, u_max);

        float rs = (u_img - u_min) / (u_max - u_min);
        float rt = (v_img - v_max) / (v_min - v_max);
        auto cBot = (1 - rs) * Q11 + rs * Q12;
        auto cTop = (1 - rs) * Q21 + rs * Q22;
        auto P = (1 - rt) * cBot + rt * cTop;

        return Eigen::Vector3f(P[0], P[1], P[2]);
    }

```

* main.cpp - texture_fragment
```c++
Eigen::Vector3f texture_fragment_shader(const fragment_shader_payload& payload)
{
    Eigen::Vector3f return_color = {0, 0, 0};
    if (payload.texture)
    {
        // TODO: Get the texture value at the texture coordinates of the current fragment
        return_color = payload.texture->getColor(payload.tex_coords.x(), payload.tex_coords.y());
    }
    Eigen::Vector3f texture_color;
    texture_color << return_color.x(), return_color.y(), return_color.z();

    Eigen::Vector3f ka = Eigen::Vector3f(0.005, 0.005, 0.005);
    Eigen::Vector3f kd = texture_color / 255.f;
    Eigen::Vector3f ks = Eigen::Vector3f(0.7937, 0.7937, 0.7937);

    auto l1 = light{{20, 20, 20}, {500, 500, 500}};
    auto l2 = light{{-20, 20, 0}, {500, 500, 500}};

    std::vector<light> lights = {l1, l2};
    Eigen::Vector3f amb_light_intensity{10, 10, 10};
    Eigen::Vector3f eye_pos{0, 0, 10};

    float p = 150;

    Eigen::Vector3f color = texture_color;
    Eigen::Vector3f point = payload.view_pos;
    Eigen::Vector3f normal = payload.normal;

    Eigen::Vector3f result_color = {0, 0, 0};

    for (auto& light : lights)
    {
        // TODO: For each light source in the code, calculate what the *ambient*, *diffuse*, and *specular* 
         // components are. Then, accumulate that result on the *result_color* object.
        Eigen::Vector3f light_dir = light.position - point;
        Eigen::Vector3f view_dir = eye_pos - point;
        float r = light_dir.dot(light_dir);
        // ambient
        Eigen::Vector3f La = ka.cwiseProduct(amb_light_intensity);
        // diffuse
        Eigen::Vector3f Ld = kd.cwiseProduct(light.intensity / r);
        Ld *= std::max(0.0f, normal.normalized().dot(light_dir.normalized()));
        // specular
        Eigen::Vector3f h = (light_dir + view_dir).normalized();
        Eigen::Vector3f Ls = ks.cwiseProduct(light.intensity / r);
        Ls *= std::pow(std::max(0.0f, normal.normalized().dot(h)), p);

        result_color += (La + Ld + Ls);

    }

    return result_color * 255.f;
}
```

* main.cpp - phong_fragment
```c++
Eigen::Vector3f phong_fragment_shader(const fragment_shader_payload& payload)
{
    Eigen::Vector3f ka = Eigen::Vector3f(0.005, 0.005, 0.005);
    Eigen::Vector3f kd = payload.color;
    Eigen::Vector3f ks = Eigen::Vector3f(0.7937, 0.7937, 0.7937);

    auto l1 = light{{20, 20, 20}, {500, 500, 500}};
    auto l2 = light{{-20, 20, 0}, {500, 500, 500}};

    std::vector<light> lights = {l1, l2};
    Eigen::Vector3f amb_light_intensity{10, 10, 10};
    Eigen::Vector3f eye_pos{0, 0, 10};

    float p = 150;

    Eigen::Vector3f color = payload.color;
    Eigen::Vector3f point = payload.view_pos;
    Eigen::Vector3f normal = payload.normal;

    Eigen::Vector3f result_color = {0, 0, 0};
    for (auto& light : lights)
    {
        // 光的方向
        Eigen::Vector3f light_dir = light.position - point;
        // 视线方向
        Eigen::Vector3f view_dir = eye_pos - point;
        // 衰减因子
        float r = light_dir.dot(light_dir);

        // ambient
        Eigen::Vector3f La = ka.cwiseProduct(amb_light_intensity);
        // diffuse
        Eigen::Vector3f Ld = kd.cwiseProduct(light.intensity / r);
        Ld *= std::max(0.0f, normal.normalized().dot(light_dir.normalized()));
        // specular
        Eigen::Vector3f h = (light_dir + view_dir).normalized();
        Eigen::Vector3f Ls = ks.cwiseProduct(light.intensity / r);
        Ls *= std::pow(std::max(0.0f, normal.normalized().dot(h)), p);

        result_color += (La + Ld + Ls);
    }

    return result_color * 255.f;
}
```

* main.cpp - phong_fragment
```c++
Eigen::Vector3f displacement_fragment_shader(const fragment_shader_payload& payload)
{
    Eigen::Vector3f ka = Eigen::Vector3f(0.005, 0.005, 0.005);
    Eigen::Vector3f kd = payload.color;
    Eigen::Vector3f ks = Eigen::Vector3f(0.7937, 0.7937, 0.7937);

    auto l1 = light{ {20, 20, 20}, {500, 500, 500} };
    auto l2 = light{ {-20, 20, 0}, {500, 500, 500} };

    std::vector<light> lights = { l1, l2 };
    Eigen::Vector3f amb_light_intensity{ 10, 10, 10 };
    Eigen::Vector3f eye_pos{ 0, 0, 10 };

    float p = 150;

    Eigen::Vector3f color = payload.color;
    Eigen::Vector3f point = payload.view_pos;
    Eigen::Vector3f normal = payload.normal;

    float kh = 0.2, kn = 0.1;

    // TODO: Implement displacement mapping here
    // Let n = normal = (x, y, z)
    // Vector t = (x*y/sqrt(x*x+z*z),sqrt(x*x+z*z),z*y/sqrt(x*x+z*z))
    // Vector b = n cross product t
    // Matrix TBN = [t b n]
    // dU = kh * kn * (h(u+1/w,v)-h(u,v))
    // dV = kh * kn * (h(u,v+1/h)-h(u,v))
    // Vector ln = (-dU, -dV, 1)
    // Position p = p + kn * n * h(u,v)
    // Normal n = normalize(TBN * ln)

    float x = normal.x();
    float y = normal.y();
    float z = normal.z();
    Eigen::Vector3f t{ x * y / std::sqrt(x * x + z * z), std::sqrt(x * x + z * z), z * y / std::sqrt(x * x + z * z) };
    Eigen::Vector3f b = normal.cross(t);
    Eigen::Matrix3f TBN;
    TBN << t.x(), b.x(), normal.x(),
        t.y(), b.y(), normal.y(),
        t.z(), b.z(), normal.z();

    float u = payload.tex_coords.x();
    float v = payload.tex_coords.y();
    float w = payload.texture->width;
    float h = payload.texture->height;


    float dU = kh * kn * (payload.texture->getColor(u + 1.0f / w, v).norm() - payload.texture->getColor(u, v).norm());
    float dV = kh * kn * (payload.texture->getColor(u, v + 1.0f / h).norm() - payload.texture->getColor(u, v).norm());

    Eigen::Vector3f ln{ -dU,-dV,1.0f };

    point += (kn * normal * payload.texture->getColor(u, v).norm());

    normal = TBN * ln;
    normal = normal.normalized();

    Eigen::Vector3f result_color = { 0, 0, 0 };

    for (auto& light : lights)
    {
        // TODO: For each light source in the code, calculate what the *ambient*, *diffuse*, and *specular* 
        // components are. Then, accumulate that result on the *result_color* object.
        Eigen::Vector3f light_dir = light.position - point;
        Eigen::Vector3f view_dir = eye_pos - point;
        float r = light_dir.dot(light_dir);

        // ambient
        Eigen::Vector3f La = ka.cwiseProduct(amb_light_intensity);
        // diffuse
        Eigen::Vector3f Ld = kd.cwiseProduct(light.intensity / r);
        Ld *= std::max(0.0f, normal.dot(light_dir.normalized()));
        // specular
        Eigen::Vector3f h = (light_dir + view_dir).normalized();
        Eigen::Vector3f Ls = ks.cwiseProduct(light.intensity / r);
        Ls *= std::pow(std::max(0.0f, normal.dot(h)), p);

        result_color += (La + Ld + Ls);

    }

    return result_color * 255.f;
}
```


* main.cpp - bump_fragment
```c++
Eigen::Vector3f bump_fragment_shader(const fragment_shader_payload& payload)
{
    Eigen::Vector3f ka = Eigen::Vector3f(0.005, 0.005, 0.005);
    Eigen::Vector3f kd = payload.color;
    Eigen::Vector3f ks = Eigen::Vector3f(0.7937, 0.7937, 0.7937);

    auto l1 = light{ {20, 20, 20}, {500, 500, 500} };
    auto l2 = light{ {-20, 20, 0}, {500, 500, 500} };

    std::vector<light> lights = { l1, l2 };
    Eigen::Vector3f amb_light_intensity{ 10, 10, 10 };
    Eigen::Vector3f eye_pos{ 0, 0, 10 };

    float p = 150;

    Eigen::Vector3f color = payload.color;
    Eigen::Vector3f point = payload.view_pos;
    Eigen::Vector3f normal = payload.normal;


    float kh = 0.2, kn = 0.1;

    // TODO: Implement bump mapping here
    // Let n = normal = (x, y, z)
    // Vector t = (x*y/sqrt(x*x+z*z),sqrt(x*x+z*z),z*y/sqrt(x*x+z*z))
    // Vector b = n cross product t
    // Matrix TBN = [t b n]
    // dU = kh * kn * (h(u+1/w,v)-h(u,v))
    // dV = kh * kn * (h(u,v+1/h)-h(u,v))
    // Vector ln = (-dU, -dV, 1)
    // Normal n = normalize(TBN * ln)

    float x = normal.x();
    float y = normal.y();
    float z = normal.z();
    Eigen::Vector3f t{ x * y / std::sqrt(x * x + z * z), std::sqrt(x * x + z * z), z * y / std::sqrt(x * x + z * z) };
    Eigen::Vector3f b = normal.cross(t);
    Eigen::Matrix3f TBN;
    TBN << t.x(), b.x(), normal.x(),
        t.y(), b.y(), normal.y(),
        t.z(), b.z(), normal.z();

    float u = payload.tex_coords.x();
    float v = payload.tex_coords.y();
    float w = payload.texture->width;
    float h = payload.texture->height;

    float dU = kh * kn * (payload.texture->getColor(u + 1.0f / w, v).norm() - payload.texture->getColor(u, v).norm());
    float dV = kh * kn * (payload.texture->getColor(u, v + 1.0f / h).norm() - payload.texture->getColor(u, v).norm());

    Eigen::Vector3f ln{ -dU,-dV,1.0f };

    normal = TBN * ln;
    // 归一化
    Eigen::Vector3f result_color = normal.normalized();
    return result_color * 255.f;
}
```

#### 四、作业4
需要实现 de Casteljau 算法来绘制由 4 个控制点表示的 Bézier 曲线 (当你正确实现该
算法时，你可以支持绘制由更多点来控制的 Bézier 曲线)。
你需要修改的函数在提供的 main.cpp 文件中。
• bezier：该函数实现绘制 Bézier 曲线的功能。它使用一个控制点序列和一个
OpenCV：：Mat 对象作为输入，没有返回值。它会使 t 在 0 到 1 的范围内进
行迭代，并在每次迭代中使 t 增加一个微小值。对于每个需要计算的 t，将
调用另一个函数 recursive_bezier，然后该函数将返回在 Bézier 曲线上 t
处的点。最后，将返回的点绘制在 OpenCV ：：Mat 对象上。
• recursive_bezier：该函数使用一个控制点序列和一个浮点数 t 作为输入，
实现 de Casteljau 算法来返回 Bézier 曲线上对应点的坐标。

要求：
• [20 分] De Casteljau 算法：
对于给定的控制点，你的代码能够产生正确的 Bézier 曲线。
• [5 分] 奖励分数：
实现对 Bézier 曲线的反走样。(对于一个曲线上的点，不只把它对应于一个像
素，你需要根据到像素中心的距离来考虑与它相邻的像素的颜色。)

可能会有的问题：需要对每一个点进行差值
``` c++
cv::Point2f recursive_bezier(const std::vector<cv::Point2f>& control_points, float t)
{
    // TODO: Implement de Casteljau's algorithm

    if (control_points.size() == 0) {
        // Error!!
        return cv::Point2f();
    }
    else if (control_points.size() == 1) {
        return control_points[0];
    }
    else{
        std::vector<cv::Point2f> points;
        for (size_t i = 0; i < control_points.size() - 1; i++)
        {
            points.push_back(control_points[i] + (control_points[i+1] - control_points[i]) * t);
        }
        return recursive_bezier(points, t);
    }
    
    return cv::Point2f();

}

void bezier(const std::vector<cv::Point2f> &control_points, cv::Mat &window) 
{
    // TODO: Iterate through all t = 0 to t = 1 with small steps, and call de Casteljau's 
    // recursive Bezier algorithm.
    for (double t = 0.0; t <= 1.0; t += 0.001)
    {
        auto point = recursive_bezier(control_points, t);
        window.at<cv::Vec3b>(point.y, point.x)[1] = 255;

        std::vector<cv::Point2f> points(4);
        points[0] = cv::Point2f(std::floor(point.x + 0.5), std::floor(point.y + 0.5));
        points[1] = cv::Point2f(std::floor(point.x + 0.5), std::floor(point.y - 0.5));
        points[2] = cv::Point2f(std::floor(point.x - 0.5), std::floor(point.y + 0.5));
        points[3] = cv::Point2f(std::floor(point.x - 0.5), std::floor(point.y - 0.5));
    
        cv::Point2f distance = points[0] - point; //距离采样点最近的像素点坐标是+0.5后的点
        float d0 = sqrt(distance.x * distance.x + distance.y * distance.y); //取这个距离作为参照
        
        for (auto p : points)
        {
            
            cv::Point2f d = p - point;
            float percnet = d0 / sqrt(d.x * d.x + d.y * d.y); //计算其他像素点与最近距离的比值
            float color = window.at<cv::Vec3b>(p.y, p.x)[1];
            color = std::max(color, 255 * percnet);//取最大值效果更好
            window.at<cv::Vec3b>(p.y, p.x)[1] = color;
        }
    }
}
```


#### 五、作业5
需要修改的函数是：
• Renderer.cpp 中的 Render()：这里你需要为每个像素生成一条对应的光
线，然后调用函数 castRay() 来得到颜色，最后将颜色存储在帧缓冲区的相
应像素中。
• Triangle.hpp 中的 rayTriangleIntersect(): v0, v1, v2 是三角形的三个
顶点，orig 是光线的起点，dir 是光线单位化的方向向量。tnear, u, v 是你需
要使用我们课上推导的 Moller-Trumbore 算法来更新的参数。

> Renderer.cpp的推导：
> 1. 将i,y 的屏幕坐标转成左下角为0，1的且以中心点0.5摆放
> 2. 将坐标系转成中心为(0,1)范围
> 3. 转为方形
> 4. 关联上fov
> 5. y轴需要反过来！
> 6. 小蓝点异常？ 将宽高-1

```c++
void Renderer::Render(const Scene& scene)
{
    std::vector<Vector3f> framebuffer(scene.width * scene.height);

    float scale = std::tan(deg2rad(scene.fov * 0.5f));
    float imageAspectRatio = scene.width / (float)scene.height;

    // Use this variable as the eye position to start your rays.
    Vector3f eye_pos(0);
    int m = 0;
    for (int j = 0; j < scene.height; ++j)
    {
        for (int i = 0; i < scene.width; ++i)
        {
            // generate primary ray direction
              // TODO: Find the x and y positions of the current pixel to get the direction
            // vector that passes through it.
            // Also, don't forget to multiply both of them with the variable *scale*, and
            // x (horizontal) variable with the *imageAspectRatio*       

            float x = (2 * ((i + 0.5) / (scene.width-1)) - 1) * imageAspectRatio * scale;
            float y =  (1 - 2 * ((j + 0.5) / (scene.height-1))) * scale;

            Vector3f dir = Vector3f(x, y, -1); // Don't forget to normalize this direction!
            framebuffer[m++] = castRay(eye_pos, dir, scene, 0);
        }
        UpdateProgress(j / (float)scene.height);
    }

    // save framebuffer to file
    FILE* fp = fopen("binary.ppm", "wb");
    (void)fprintf(fp, "P6\n%d %d\n255\n", scene.width, scene.height);
    for (auto i = 0; i < scene.height * scene.width; ++i) {
        static unsigned char color[3];
        color[0] = (char)(255 * clamp(0, 1, framebuffer[i].x));
        color[1] = (char)(255 * clamp(0, 1, framebuffer[i].y));
        color[2] = (char)(255 * clamp(0, 1, framebuffer[i].z));
        fwrite(color, 1, 3, fp);
    }
    fclose(fp);    
}
```

Moller Trumbore 算法来求光线是否在与平面有交点，使用重点坐标
![Moller Trumbore](/img/160880489472851363.png)

```c++

bool rayTriangleIntersect(const Vector3f& v0, const Vector3f& v1, const Vector3f& v2, const Vector3f& orig,
                          const Vector3f& dir, float& tnear, float& u, float& v)
{
    // TODO: Implement this function that tests whether the triangle
    // that's specified bt v0, v1 and v2 intersects with the ray (whose
    // origin is *orig* and direction is *dir*)
    // Also don't forget to update tnear, u and v.
    auto e1 = v1 - v0;
    auto e2 = v2 - v0;
    auto s = orig - v0;
    auto s1 = crossProduct(dir, e2);
    auto s2 = crossProduct(s, e1);
    float t = dotProduct(s2, e2) / dotProduct(s1, e1);
    float b1 = dotProduct(s1, s) / dotProduct(s1, e1);
    float b2 = dotProduct(s2, dir) / dotProduct(s1, e1);
    if (t > 0 && b1 > 0 && b2 > 0 && (1 - b1 - b2) > 0) {
        tnear = t;
        u = b1;
        v = b2;
        return true;
    }

    return false;
}
```

> 生成的Ppm需要用此工具打开 https://www.fosshub.com/IrfanView.html?dwl=iview460_x64_setup.exe

#### 六、作业6
本练习要求你实现 Ray-Bounding
Volume 求交与 BVH 查找。
首先，你需要从上一次编程练习中引用以下函数：
• Render() in Renderer.cpp: 将你的光线生成过程粘贴到此处，并且按照新框
架更新相应调用的格式。
• Triangle::getIntersection in Triangle.hpp: 将你的光线-三角形相交函数
粘贴到此处，并且按照新框架更新相应相交信息的格式。

在本次编程练习中，你需要实现以下函数：
• IntersectP(const Ray& ray, const Vector3f& invDir,
const std::array<int, 3>& dirIsNeg) in the Bounds3.hpp: 这个函数的
作用是判断包围盒 BoundingBox 与光线是否相交，你需要按照课程介绍的算
法实现求交过程。
• getIntersection(BVHBuildNode* node, const Ray ray)in BVH.cpp: 建
立 BVH 之后，我们可以用它加速求交过程。该过程递归进行，你将在其中调
用你实现的 Bounds3::IntersectP.

```c++
inline Intersection Triangle::getIntersection(Ray ray)
{
    Intersection inter;

    if (dotProduct(ray.direction, normal) > 0)
        return inter;
    double u, v, t_tmp = 0;
    Vector3f pvec = crossProduct(ray.direction, e2);
    double det = dotProduct(e1, pvec);
    if (fabs(det) < EPSILON)
        return inter;

    double det_inv = 1. / det;
    Vector3f tvec = ray.origin - v0;
    u = dotProduct(tvec, pvec) * det_inv;
    if (u < 0 || u > 1)
        return inter;
    Vector3f qvec = crossProduct(tvec, e1);
    v = dotProduct(ray.direction, qvec) * det_inv;
    if (v < 0 || u + v > 1)
        return inter;
    t_tmp = dotProduct(e2, qvec) * det_inv;

    // TODO find ray triangle intersection
    /*
    * 
    coords：光线经过的那一点的坐标，这里使用ray（double）（注意，我们在Ray.h中重载了（），用于计算t时刻的光线坐标）
    happend：光线和三角形是否相交？
    m：材质
    normal：交点处三角形的法线
    distance：光线经过的时间，也就是我们算出来的t_tmp。
    object：事实上你进入Objects.h,就会发现基类Object（接口，里面一堆纯虚函数），这里作为一个指针，指向本对象，也就是this（框架的编程还是很漂亮的），指代我们的三角形。
    */
    if (t_tmp < 0)
        return inter;
    inter.distance = t_tmp;
    inter.happened = true;
    inter.m = m;
    inter.obj = this;
    inter.normal = normal;
    inter.coords = ray(t_tmp);
    return inter;
}

void Renderer::Render(const Scene& scene)
{
    std::vector<Vector3f> framebuffer(scene.width * scene.height);

    float scale = tan(deg2rad(scene.fov * 0.5));
    float imageAspectRatio = scene.width / (float)scene.height;
    Vector3f eye_pos(-1, 5, 10);
    int m = 0;
    for (uint32_t j = 0; j < scene.height; ++j) {
        for (uint32_t i = 0; i < scene.width; ++i) {
            // generate primary ray direction
            float x = (2 * (i + 0.5) / (float)scene.width - 1) *
                      imageAspectRatio * scale;
            float y = (1 - 2 * (j + 0.5) / (float)scene.height) * scale;
            
            Vector3f dir = Vector3f(x, y, -1);
            // Don't forget to normalize this direction!
            dir = normalize(dir);
            Ray ray(eye_pos, dir);
            framebuffer[m++] = scene.castRay(ray, 0);
        }
        UpdateProgress(j / (float)scene.height);
    }
    UpdateProgress(1.f);

    // save framebuffer to file
    FILE* fp = fopen("binary.ppm", "wb");
    (void)fprintf(fp, "P6\n%d %d\n255\n", scene.width, scene.height);
    for (auto i = 0; i < scene.height * scene.width; ++i) {
        static unsigned char color[3];
        color[0] = (unsigned char)(255 * clamp(0, 1, framebuffer[i].x));
        color[1] = (unsigned char)(255 * clamp(0, 1, framebuffer[i].y));
        color[2] = (unsigned char)(255 * clamp(0, 1, framebuffer[i].z));
        fwrite(color, 1, 3, fp);
    }
    fclose(fp);    
}

inline bool Bounds3::IntersectP(const Ray& ray, const Vector3f& invDir,
                                const std::array<int, 3>& dirIsNeg) const
{
    // invDir: ray direction(x,y,z), invDir=(1.0/x,1.0/y,1.0/z), use this because Multiply is faster that Division
    // dirIsNeg: ray direction(x,y,z), dirIsNeg=[int(x>0),int(y>0),int(z>0)], use this to simplify your logic
    // TODO test if ray bound intersects
    
    float t_Min_x = (pMin.x - ray.origin.x) * invDir[0];
    float t_Min_y = (pMin.y - ray.origin.y) * invDir[1];
    float t_Min_z = (pMin.z - ray.origin.z) * invDir[2];
    float t_Max_x = (pMax.x - ray.origin.x) * invDir[0];
    float t_Max_y = (pMax.y - ray.origin.y) * invDir[1];
    float t_Max_z = (pMax.z - ray.origin.z) * invDir[2];
    if (!dirIsNeg[0])
    {
        float t = t_Min_x;
        t_Min_x = t_Max_x;
        t_Max_x = t;
    }
    if (!dirIsNeg[1])
    {
        float t = t_Min_y;
        t_Min_y = t_Max_y;
        t_Max_y = t;
    }
    if (!dirIsNeg[2])
    {
        float t = t_Min_z;
        t_Min_z = t_Max_z;
        t_Max_z = t;
    }

    float t_enter = std::max(t_Min_x, std::max(t_Min_y, t_Min_z));
    float t_exit = std::min(t_Max_x, std::min(t_Max_y, t_Max_z));
    if (t_enter < t_exit && t_exit >= 0)
        return true;
    else
        return false;
}

Intersection BVHAccel::getIntersection(BVHBuildNode* node, const Ray& ray) const
{
    // TODO Traverse the BVH to find intersection

    Intersection intersect;
    Vector3f invdir(1. / ray.direction.x, 1. / ray.direction.y, 1. / ray.direction.z);
    std::array<int, 3> dirIsNeg;
    dirIsNeg[0] = ray.direction.x > 0;
    dirIsNeg[1] = ray.direction.y > 0;
    dirIsNeg[2] = ray.direction.z > 0;
    if (!node->bounds.IntersectP(ray, invdir, dirIsNeg))
    {
        return intersect;
    }
    // 根据BVH的定义可知，当为叶子结点时，说明此为最小相交Object
    if (node->left == nullptr && node->right == nullptr)
    {
        return node->object->getIntersection(ray);
    }
    Intersection h1 = getIntersection(node->left, ray);
    Intersection h2 = getIntersection(node->right, ray);
    return h1.distance < h2.distance ? h1 : h2;
    return intersect;

}
```

SAH的方式： 参考 https://www.cnblogs.com/coolwx/p/14375763.html
```c++
BVHBuildNode* BVHAccel::recursiveBuild(std::vector<Object*>objects)
{
    BVHBuildNode* node = new BVHBuildNode();

    // Compute bounds of all primitives in BVH node
    Bounds3 bounds;
    for (int i = 0; i < objects.size(); ++i)
        bounds = Union(bounds, objects[i]->getBounds());
    if (objects.size() == 1) {
        // Create leaf _BVHBuildNode_
        node->bounds = objects[0]->getBounds();
        node->object = objects[0];
        node->left = nullptr;
        node->right = nullptr;
        return node;
    }
    else if (objects.size() == 2) {
        node->left = recursiveBuild(std::vector{ objects[0] });
        node->right = recursiveBuild(std::vector{ objects[1] });

        node->bounds = Union(node->left->bounds, node->right->bounds);
        return node;
    }
    else
    {
        Bounds3 centroidBounds;
        //算出最大的包围盒（通用的，因为两个方法都要用到）
        for (int i = 0; i < objects.size(); ++i)
            centroidBounds =
            Union(centroidBounds, objects[i]->getBounds().Centroid());

        std::vector<Object*> leftshapes;
        std::vector<Object*> rightshapes;

        switch (splitMethod)//这里注意了在BVH.h里面有个枚举类，构造函数中的初始将决定是普通方法，还是SAH
        {
        case SplitMethod::NAIVE:
        {
            int dim = centroidBounds.maxExtent();//算出最大的跨度对应的值，x为0，y为1，z为2
            int index = objects.size() / 2;
            switch (dim)
                //排序，针对最大的跨度排序
            {
            case 0:
                std::sort(objects.begin(), objects.end(), [](auto f1, auto f2) {
                    return f1->getBounds().Centroid().x <
                        f2->getBounds().Centroid().x;
                    });
                break;
            case 1:
                std::sort(objects.begin(), objects.end(), [](auto f1, auto f2) {
                    return f1->getBounds().Centroid().y <
                        f2->getBounds().Centroid().y;
                    });
                break;
            case 2:
                std::sort(objects.begin(), objects.end(), [](auto f1, auto f2) {
                    return f1->getBounds().Centroid().z <
                        f2->getBounds().Centroid().z;
                    });
                break;
            }

            auto beginning = objects.begin();
            auto middling = objects.begin() + index;
            auto ending = objects.end();
            //递归算法，枢轴是中间元素。
            leftshapes = std::vector<Object*>(beginning, middling);
            rightshapes = std::vector<Object*>(middling, ending);
        }
        break;
        case SplitMethod::SAH:
        {
            float nArea = centroidBounds.SurfaceArea();//算出最大的

            int minCostCoor = 0;
            int mincostIndex = 0;
            float minCost = std::numeric_limits<float>::infinity();
            std::map<int, std::map<int, int>> indexMap;
            //indexmap用于记录x，y，z（前一个int代表x，y，z，后一个map代表那个轴对应的map）
            //遍历x，y，z的划分
            for (int i = 0; i < 3; i++)
            {
                int bucketCount = 12;//桶的个数，这里定了12个桶，就是在某一个轴上面划分了12个区域
                std::vector<Bounds3> boundsBuckets;
                std::vector<int> countBucket;
                for (int j = 0; j < bucketCount; j++)
                {
                    boundsBuckets.push_back(Bounds3());
                    countBucket.push_back(0);
                }

                std::map<int, int> objMap;
                for (int j = 0; j < objects.size(); j++)
                {
                    Vector3f objCentroidOffset = centroidBounds.Offset(objects[j]->getBounds().Centroid());
                    double v = objCentroidOffset[i];
                    int bid = bucketCount * v;//算出对应x，y。z上的id值，这里【i】代表x，y，z
                    if (bid > bucketCount - 1)//实质是可以划分13个区域的，将最后一个区域合并。
                    {
                        bid = bucketCount - 1;
                    }
                    Bounds3 b = boundsBuckets[bid];
                    b = Union(b, objects[j]->getBounds().Centroid());
                    boundsBuckets[bid] = b;
                    countBucket[bid] = countBucket[bid] + 1;
                    objMap.insert(std::make_pair(j, bid));
                }

                indexMap.insert(std::make_pair(i, objMap));
                //对于每一个划分，计算他所对应的花费，方法是对于桶中的每一个面积，计算他的花费，最后进行计算
                //找出这个划分。
                for (int j = 1; j < boundsBuckets.size(); j++)
                {
                    Bounds3 A;
                    Bounds3 B;
                    int countA = 0;
                    int countB = 0;
                    for (int k = 0; k < j; k++)
                    {
                        A = Union(A, boundsBuckets[k]);
                        countA += countBucket[k];
                    }

                    for (int k = j; k < boundsBuckets.size(); k++)
                    {
                        B = Union(B, boundsBuckets[k]);
                        countB += countBucket[k];
                    }

                    float cost = 1 + (countA * A.SurfaceArea() + countB * B.SurfaceArea()) / nArea;//计算花费
                    //找出这个最小花费。
                    if (cost < minCost)
                    {
                        minCost = cost;
                        mincostIndex = j;
                        minCostCoor = i;
                    }
                }
                //以上得出的是一个轴的mincostIndex
            }
            // 找出最理想的花费方式的值，以此为中间，分出左右树
            for (int i = 0; i < objects.size(); i++)
            {
                if (indexMap[minCostCoor][i] < mincostIndex)
                {
                    leftshapes.push_back(objects[i]);
                }
                else
                {
                    rightshapes.push_back(objects[i]);
                }
            }
        }
        break;
    default:
        break;
        }

        assert(objects.size() == (leftshapes.size() + rightshapes.size()));
        //递归计算，同普通方法
        node->left = recursiveBuild(leftshapes);
        node->right = recursiveBuild(rightshapes);

        node->bounds = Union(node->left->bounds, node->right->bounds);
    }

    return node;
}
```
> SAH的方式，精髓在于把一个轴向分成一定数量的桶，在把所有物体根据重心坐标的偏移分到这些桶里，再用公式找到以哪个桶为中心时COST最低。 这是一个轴的，再将另外几个轴按相同算法算出。最后取最划算的轴和最划算的中心位置桶，得出最终的高效的BVH结构。
> 课件的例子中，如果使用NAIVE方法，构建自然更快，但最终render时会慢。对于更复杂的场景，SAH的效果将会更好。

#### 七、作业7
路径追踪

本次实验中，你只需要修改这一个函数:
• castRay(const Ray ray, int depth)in Scene.cpp: 在其中实现 Path Tracing 算法
可能用到的函数有：
• intersect(const Ray ray)in Scene.cpp: 求一条光线与场景的交点
• sampleLight(Intersection pos, float pdf) in Scene.cpp: 在场景的所有
光源上按面积 uniform 地 sample 一个点，并计算该 sample 的概率密度
3
• sample(const Vector3f wi, const Vector3f N) in Material.cpp: 按照该
材质的性质，给定入射方向与法向量，用某种分布采样一个出射方向
• pdf(const Vector3f wi, const Vector3f wo, const Vector3f N) in Material.cpp: 给定一对入射、出射方向与法向量，计算 sample 方法得到该出射
方向的概率密度
• eval(const Vector3f wi, const Vector3f wo, const Vector3f N) in Material.cpp: 给定一对入射、出射方向与法向量，计算这种情况下的 f_r 值
可能用到的变量有：
• RussianRoulette in Scene.cpp: P_RR, Russian Roulette 的概率

 ![参考流程](/img/1608804894728513113.png)
  ![最终效果 30SPP](/img/1608804894728513114.png)
参考： https://www.bilibili.com/read/cv12184818/
 ```c++
 // IntersectionP的实现，正确的方式
 inline bool Bounds3::IntersectP(const Ray& ray, const Vector3f& invDir,
                                const std::array<int, 3>& dirIsNeg) const
{
    // invDir: ray direction(x,y,z), invDir=(1.0/x,1.0/y,1.0/z), use this because Multiply is faster that Division
    // dirIsNeg: ray direction(x,y,z), dirIsNeg=[int(x>0),int(y>0),int(z>0)], use this to simplify your logic
    // TODO test if ray bound intersects
    float t_inX, t_outX, t_inY, t_outY, t_inZ, t_outZ;
    if (ray.direction.x > 0) {
        t_inX = (pMin.x - ray.origin.x) * invDir.x;
        t_outX = (pMax.x - ray.origin.x) * invDir.x;

    }
    else if (ray.direction.x == 0.0) {
        t_inX = FLT_MAX;
        t_outX = FLT_MAX;

    }
    else {
        t_outX = (pMin.x - ray.origin.x) * invDir.x;
        t_inX = (pMax.x - ray.origin.x) * invDir.x;
    }

    if (ray.direction.y > 0) {
        t_inY = (pMin.y - ray.origin.y) * invDir.y;
        t_outY = (pMax.y - ray.origin.y) * invDir.y;

    }
    else if (ray.direction.y == 0.0) {
        t_inY = FLT_MAX;
        t_outY = FLT_MAX;

    }
    else {
        t_outY = (pMin.y - ray.origin.y) * invDir.y;
        t_inY = (pMax.y - ray.origin.y) * invDir.y;
    }

    if (ray.direction.z > 0) {
        t_inZ = (pMin.z - ray.origin.z) * invDir.z;
        t_outZ = (pMax.z - ray.origin.z) * invDir.z;

    }
    else if (ray.direction.z == 0.0) {
        t_inZ = FLT_MAX;
        t_outZ = FLT_MAX;

    }
    else {
        t_outZ = (pMin.z - ray.origin.z) * invDir.z;
        t_inZ = (pMax.z - ray.origin.z) * invDir.z;
    }
    float t_min = std::max(std::max(t_inX, t_inY), t_inZ);
    float t_max = std::min(std::min(t_outX, t_outY), t_outZ);

    if (t_max >= t_min && t_max >= 0)
        return true;
    return false;
}
//核心实现 Scene.cpp
// Implementation of Path Tracing
Vector3f Scene::castRay(const Ray &ray, int depth) const
{
    float pdf;
    Vector3f color1 = { .0,.0,.0 }, color2 = { .0,.0,.0 };
    Intersection intersection = Scene::intersect(ray);
    //找不到这个投射点，直接返回
    if (!intersection.happened) {
        return {};
    }
    //如果射线打到光   //hasEmission函数m->m_emission向量的距离是否大于0.00001}
    //在main中定义了光材质Material* light = new Material(DIFFUSE, Vector3f(0.747f+0.058f, 0.747f+0.258f, 0.747f)....);
    //其他材质创建时 第二个传参值都是Vector3f(0.0f); 第二传参值定义了m->m_emission也就是说除了光其他 调用 hasEmission函数都是false
    if (intersection.m->hasEmission()) {
        return intersection.m->m_emission;
    }//之后的都是 有投射点且不是光

    Material* mater = intersection.m;
    Intersection light_inter;
    sampleLight(light_inter, pdf);
    Vector3f light_point_v3 = light_inter.coords - intersection.coords;
    Vector3f point_light_dir = light_point_v3.normalized();
    float point_light_dis_pow2 = light_point_v3.x * light_point_v3.x + light_point_v3.y * light_point_v3.y + light_point_v3.z * light_point_v3.z;
    float point_light_dis = std::sqrt(point_light_dis_pow2);
    //光比物体近   还要考虑物体和光距离一样的情况  这里还是看别人写的才发现的 的确考虑不周
        //进度问题 这里写成了>= -0.005f  写小了就会有横条
    if ((intersect(Ray(intersection.coords, point_light_dir)).distance - point_light_dis)
        >= -0.005f) {
        //需知 光源烈度 * BRDF * cos(交点法线,交点到光方向) * cos(光源法线,-交点到光方向)  / PDF / 距离^2
        color1 = light_inter.emit
            * mater->eval(ray.direction, point_light_dir, intersection.normal)
            * dotProduct(intersection.normal, point_light_dir)
            * dotProduct(light_inter.normal, -point_light_dir)
            / pdf
            / point_light_dis_pow2;
    }
    float p = (float)(rand() % 100) / 100;
    if (p > RussianRoulette) {
        return color1;
    }
    Vector3f l_exit_dir = mater->sample(ray.direction, intersection.normal);
    Ray l_exit = Ray(intersection.coords, l_exit_dir);
    Intersection inter_sequel = intersect(l_exit);
    //如何判断这个射线射没射到光源?
    if (inter_sequel.happened && !inter_sequel.m->hasEmission()) {
        color2 = castRay(l_exit, depth + 1)
            * mater->eval(ray.direction, l_exit_dir, intersection.normal)
            * dotProduct(intersection.normal, l_exit_dir)
            / mater->pdf(ray.direction, l_exit_dir, intersection.normal)
            / RussianRoulette;
    }
    return color1 + color2;
}

 //Sphere.hpp
 Intersection getIntersection(Ray ray){
        Intersection result;
        result.happened = false;
        Vector3f L = ray.origin - center;
        float a = dotProduct(ray.direction, ray.direction);
        float b = 2 * dotProduct(ray.direction, L);
        float c = dotProduct(L, L) - radius2;
        float t0, t1;
        if (!solveQuadratic(a, b, c, t0, t1)) return result;
        if (t0 < 0) t0 = t1;
        if (t0 < 0) return result;
        
        //提升球体的相交判定精度
        if(t0 > 0.5){
            result.happened=true;

            result.coords = Vector3f(ray.origin + ray.direction * t0);
            result.normal = normalize(Vector3f(result.coords - center));
            result.m = this->m;
            result.obj = this;
            result.distance = t0;
        }
        return result;

    }
// 多线程
void Renderer::Render(const Scene& scene)
{
    std::vector<Vector3f> framebuffer(scene.width * scene.height);

    float scale = tan(deg2rad(scene.fov * 0.5));
    float imageAspectRatio = scene.width / (float)scene.height;
    Vector3f eye_pos(278, 273, -800);
    int m = 0;


    // change the spp value to change sample ammount
    int spp = 16;
    std::cout << "SPP: " << spp << "\n";
    const int num_threads = 32;
    std::thread th[num_threads];
    int thread_height = scene.height / num_threads;
    auto renderRows = [&](uint32_t start_height, uint32_t end_height) {
        for (uint32_t j = start_height; j < end_height; ++j) {
            for (uint32_t i = 0; i < scene.width; ++i) {
                // generate primary ray direction
                float x = (2 * (i + 0.5) / (float)scene.width - 1) *
                    imageAspectRatio * scale;
                float y = (1 - 2 * (j + 0.5) / (float)scene.height) * scale;

                Vector3f dir = normalize(Vector3f(-x, y, 1));
                for (int k = 0; k < spp; k++) {
                    framebuffer[(int)(j * scene.width + i)] += scene.castRay(Ray(eye_pos, dir), 0) / spp;
                }
            }
            mtx.lock();
            progress++;
            UpdateProgress(progress / (float)scene.height);
            mtx.unlock();
        }};
    for (int t = 0; t < num_threads; ++t) {
        th[t] = std::thread(renderRows, t * thread_height, (t + 1) * thread_height);
    }
    for (int t = 0; t < num_threads; ++t) {
        th[t].join();
    }

    UpdateProgress(1.f);

    // save framebuffer to file
    FILE* fp = fopen("binary.ppm", "wb");
    (void)fprintf(fp, "P6\n%d %d\n255\n", scene.width, scene.height);
    for (auto i = 0; i < scene.height * scene.width; ++i) {
        static unsigned char color[3];
        color[0] = (unsigned char)(255 * std::pow(clamp(0, 1, framebuffer[i].x), 0.6f));
        color[1] = (unsigned char)(255 * std::pow(clamp(0, 1, framebuffer[i].y), 0.6f));
        color[2] = (unsigned char)(255 * std::pow(clamp(0, 1, framebuffer[i].z), 0.6f));
        fwrite(color, 1, 3, fp);
    }
    fclose(fp);
}
//微表面：参考：https://blog.csdn.net/qq_36242312/article/details/116307626?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-116307626-blog-121942469.pc_relevant_multi_platform_featuressortv2dupreplace&spm=1001.2101.3001.4242.1&utm_relevant_index=3
float DistributionGGX(Vector3f N, Vector3f H, float roughness)
{
    float a = roughness * roughness;
    float a2 = a * a;
    float NdotH = std::max(dotProduct(N, H), 0.0f);
    float NdotH2 = NdotH * NdotH;

    float nom = a2;
    float denom = (NdotH2 * (a2 - 1.0) + 1.0);
    denom = M_PI * denom * denom;

    return nom / std::max(denom, 0.0000001f); // prevent divide by zero for roughness=0.0 and NdotH=1.0
}

float GeometrySchlickGGX(float NdotV, float roughness)
{
    float r = (roughness + 1.0);
    float k = (r * r) / 8.0;

    float nom = NdotV;
    float denom = NdotV * (1.0 - k) + k;

    return nom / denom;
}

float GeometrySmith(Vector3f N, Vector3f V, Vector3f L, float roughness)
{
    float NdotV = std::max(dotProduct(N, V), 0.0f);
    float NdotL = std::max(dotProduct(N, L), 0.0f);
    float ggx2 = GeometrySchlickGGX(NdotV, roughness);
    float ggx1 = GeometrySchlickGGX(NdotL, roughness);

    return ggx1 * ggx2;
}
Vector3f Material::eval(const Vector3f &wi, const Vector3f &wo, const Vector3f &N){
    switch(m_type){
        case DIFFUSE:
        {
            // calculate the contribution of diffuse   model
            float cosalpha = dotProduct(N, wo);
            if (cosalpha > 0.0f) {
                Vector3f diffuse = Kd / M_PI;
                return diffuse;
            }
            else
                return Vector3f(0.0f);
            break;
        }
        case Microfacet:
        {
            // Disney PBR 方案
            float cosalpha = dotProduct(N, wo);
            if (cosalpha > 0.0f) {
                float roughness = 0.35;

                Vector3f V = -wi;
                Vector3f L = wo;
                Vector3f H = normalize(V + L);

                // 计算 distribution of normals: D
                float D = DistributionGGX(N, H, roughness);

                // 计算 shadowing masking term: G
                float G = GeometrySmith(N, V, L, roughness);

                // 计算 fresnel 系数: F
                float F;
                float etat = 1.85;
                fresnel(wi, N, etat, F);

                Vector3f nominator = D * G * F;
                float denominator = 4 * std::max(dotProduct(N, V), 0.0f) * std::max(dotProduct(N, L), 0.0f);
                Vector3f specular = nominator / std::max(denominator, 0.001f);

                // 能量守恒
                float ks_ = F;
                float kd_ = 1.0f - ks_;

                Vector3f diffuse = 1.0f / M_PI;

                // 因为在 specular 项里已经考虑了折射部分的比例：F，所以折射部分不需要再乘以 ks_ （ks_ * Ks * specular）
                return Ks * specular + kd_ * Kd * diffuse;
            }
            else
                return Vector3f(0.0f);
            break;
        }
    }
}
 ```