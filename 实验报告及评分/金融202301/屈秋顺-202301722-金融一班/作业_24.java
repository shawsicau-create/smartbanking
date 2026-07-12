package com.example.crm.entity;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

/**
 * 客户实体类
 */
@Entity
@Table(name = "customers")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class Customer {

    /**
     * 客户编号（主键，自增）
     */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long customerId;

    /**
     * 客户姓名
     */
    @Column(nullable = false, length = 100)
    private String name;

    /**
     * 联系电话
     */
    @Column(nullable = false, length = 20)
    private String phone;

    /**
     * 电子邮箱
     */
    @Column(length = 100)
    private String email;

    /**
     * 客户等级（VIP/金卡/普通客户）
     */
    @Column(length = 20)
    private String level;

    /**
     * 开户日期
     */
    @Column(nullable = false)
    private LocalDateTime registerDate;

    /**
     * 创建时间
     */
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    /**
     * 更新时间
     */
    @Column(nullable = false)
    private LocalDateTime updatedAt;

    /**
     * 保存前自动设置创建时间和更新时间
     */
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
        if (registerDate == null) {
            registerDate = LocalDateTime.now();
        }
        if (level == null) {
            level = "普通客户";
        }
    }

    /**
     * 更新前自动设置更新时间
     */
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}